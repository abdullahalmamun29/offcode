"""
CHUP Phase 3P — Standalone C++17 Generator for Number Theory & Combinatorics.

Generates standalone, fast I/O, 64-bit safe implementations with automatic
__int128_t intermediate casting for large modular products and CRT LCM tracking,
and unsigned long long for 64-bit Miller-Rabin primality testing.
"""

from typing import Dict, Any, Optional


def generate_nt_cpp(pattern: str, model_or_params: Optional[Any] = None) -> str:
    """
    Generates high-performance, competitive-programming standard C++17 implementations
    for all Phase 3P Number Theory and Combinatorics patterns.
    """
    if pattern in ("nt_extended_gcd", "nt_diophantine"):
        return _generate_extended_gcd()
    elif pattern in ("nt_modular_inverse", "nt_modular_inverse_extgcd", "nt_modular_inverse_fermat"):
        return _generate_modular_inverse()
    elif pattern in ("nt_chinese_remainder", "nt_crt"):
        return _generate_chinese_remainder()
    elif pattern in ("nt_linear_sieve", "nt_prime_factorization"):
        return _generate_linear_sieve()
    elif pattern in ("nt_euler_totient", "nt_phi", "nt_euler_totient_single", "nt_euler_totient_sieve"):
        return _generate_euler_totient()
    elif pattern in ("nt_mobius_inversion", "nt_mobius_sieve"):
        return _generate_mobius_inversion()
    elif pattern in ("nt_matrix_power", "nt_matrix_exponentiation", "nt_linear_recurrence"):
        return _generate_matrix_power()
    elif pattern in ("nt_combinatorics_factorials", "nt_ncr_mod_p", "nt_factorial_combinatorics"):
        return _generate_combinatorics_factorials()
    elif pattern in ("nt_lucas_theorem", "nt_lucas"):
        return _generate_lucas_theorem()
    elif pattern in ("nt_miller_rabin", "nt_primality_test"):
        return _generate_miller_rabin()
    else:
        return _generate_extended_gcd()


def _generate_extended_gcd() -> str:
    return """#include <iostream>

using namespace std;

// Extended Euclidean Algorithm: computes g = gcd(a, b) and x, y such that a*x + b*y = g (g >= 0)
long long ext_gcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) {
        if (a >= 0) {
            x = 1; y = 0; return a;
        } else {
            x = -1; y = 0; return -a;
        }
    }
    long long x1, y1;
    long long g = ext_gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long a, b, c;
    if (!(cin >> a >> b >> c)) return 0;

    if (a == 0 && b == 0) {
        if (c == 0) {
            cout << 0 << " " << 0 << " " << 0 << "\\n";
        } else {
            cout << "IMPOSSIBLE\\n";
        }
        return 0;
    }

    long long x, y;
    long long g = ext_gcd(a, b, x, y);

    if (c % g != 0) {
        cout << "IMPOSSIBLE\\n";
        return 0;
    }

    long long factor = c / g;
    long long x0 = x * factor;
    long long y0 = y * factor;

    // General solution: x = x0 + (b / g) * t, y = y0 - (a / g) * t
    cout << x0 << " " << y0 << " " << g << "\\n";

    return 0;
}
"""


def _generate_modular_inverse() -> str:
    return """#include <iostream>

using namespace std;

// Extended Euclidean Algorithm
long long ext_gcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) {
        if (a >= 0) {
            x = 1; y = 0; return a;
        } else {
            x = -1; y = 0; return -a;
        }
    }
    long long x1, y1;
    long long g = ext_gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

// Modular Multiplicative Inverse: finds x such that a * x = 1 (mod m)
long long mod_inverse(long long a, long long m) {
    if (m <= 1) return -1;
    a = (a % m + m) % m;
    long long x, y;
    long long g = ext_gcd(a, m, x, y);
    if (g != 1) return -1; // Inverse does not exist when gcd(a, m) != 1
    return (x % m + m) % m;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long a, m;
    if (!(cin >> a >> m)) return 0;

    long long inv = mod_inverse(a, m);
    if (inv == -1) {
        cout << -1 << "\\n";
    } else {
        cout << inv << "\\n";
    }

    return 0;
}
"""


def _generate_chinese_remainder() -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

// Helper to print 128-bit integer
void print_int128(__int128_t x) {
    if (x == 0) { cout << 0 << "\\n"; return; }
    if (x < 0) { cout << '-'; x = -x; }
    string s;
    while (x > 0) {
        s.push_back('0' + (int)(x % 10));
        x /= 10;
    }
    for (int i = (int)s.size() - 1; i >= 0; i--) cout << s[i];
    cout << "\\n";
}

__int128_t ext_gcd128(__int128_t a, __int128_t b, __int128_t &x, __int128_t &y) {
    if (b == 0) {
        if (a >= 0) { x = 1; y = 0; return a; }
        else { x = -1; y = 0; return -a; }
    }
    __int128_t x1, y1;
    __int128_t g = ext_gcd128(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    if (!(cin >> k)) return 0;

    vector<pair<__int128_t, __int128_t>> cong;
    for (int i = 0; i < k; i++) {
        long long r, m;
        cin >> r >> m;
        cong.push_back({(__int128_t)r, (__int128_t)m});
    }

    if (cong.empty()) {
        cout << 0 << "\\n";
        return 0;
    }

    __int128_t cur_r = (cong[0].first % cong[0].second + cong[0].second) % cong[0].second;
    __int128_t cur_m = cong[0].second;

    bool possible = true;
    for (int i = 1; i < k; i++) {
        __int128_t r2 = (cong[i].first % cong[i].second + cong[i].second) % cong[i].second;
        __int128_t m2 = cong[i].second;

        __int128_t p, q;
        __int128_t g = ext_gcd128(cur_m, m2, p, q);
        __int128_t diff = r2 - cur_r;

        if (diff % g != 0) {
            possible = false;
            break;
        }

        __int128_t step = m2 / g;
        __int128_t mult = ((diff / g) % step * (p % step)) % step;
        mult = (mult + step) % step;

        __int128_t new_m = (cur_m / g) * m2;
        cur_r = (cur_r + cur_m * mult) % new_m;
        cur_m = new_m;
    }

    if (!possible) {
        cout << -1 << "\\n";
    } else {
        print_int128(cur_r);
    }

    return 0;
}
"""


def _generate_linear_sieve() -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

const int MAXN = 10000000;
int spf[MAXN + 1];
vector<int> primes;

void linear_sieve(int n) {
    for (int i = 2; i <= n; i++) {
        if (spf[i] == 0) {
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            if (p > spf[i] || (long long)i * p > n) break;
            spf[i * p] = p;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    int limit = min(n, MAXN);
    linear_sieve(limit);

    cout << primes.size() << "\\n";
    return 0;
}
"""


def _generate_euler_totient() -> str:
    return """#include <iostream>

using namespace std;

// Computes Euler's Totient phi(N) via O(sqrt(N)) trial factorization
long long euler_totient(long long n) {
    if (n <= 0) return 0;
    long long ans = n;
    for (long long d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            while (n % d == 0) n /= d;
            ans -= ans / d;
        }
    }
    if (n > 1) {
        ans -= ans / n;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    cout << euler_totient(n) << "\\n";
    return 0;
}
"""


def _generate_mobius_inversion() -> str:
    return """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAXN = 1000000;
int spf[MAXN + 1];
int mu[MAXN + 1];
vector<int> primes;

void mobius_sieve(int n) {
    mu[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (spf[i] == 0) {
            spf[i] = i;
            mu[i] = -1;
            primes.push_back(i);
        }
        for (int p : primes) {
            if (p > spf[i] || i * p > n) break;
            spf[i * p] = p;
            if (i % p == 0) {
                mu[i * p] = 0;
            } else {
                mu[i * p] = -mu[i];
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, m;
    if (!(cin >> n >> m)) return 0;

    long long lim = min(n, m);
    int sieve_lim = min((long long)MAXN, lim);
    mobius_sieve(sieve_lim);

    // Sum_{d=1}^{min(n, m)} mu(d) * floor(n/d) * floor(m/d)
    long long coprime_pairs = 0;
    for (int d = 1; d <= sieve_lim; d++) {
        if (mu[d] != 0) {
            coprime_pairs += (long long)mu[d] * (n / d) * (m / d);
        }
    }

    cout << coprime_pairs << "\\n";
    return 0;
}
"""


def _generate_matrix_power() -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

typedef vector<vector<long long>> Matrix;

Matrix multiply(const Matrix &A, const Matrix &B, long long mod) {
    int d = A.size();
    Matrix C(d, vector<long long>(d, 0));
    for (int i = 0; i < d; i++) {
        for (int k = 0; k < d; k++) {
            if (A[i][k] == 0) continue;
            for (int j = 0; j < d; j++) {
                C[i][j] = (C[i][j] + (__int128_t)A[i][k] * B[k][j]) % mod;
            }
        }
    }
    return C;
}

Matrix matrix_pow(Matrix A, long long k, long long mod) {
    int d = A.size();
    Matrix res(d, vector<long long>(d, 0));
    for (int i = 0; i < d; i++) res[i][i] = 1 % mod;
    while (k > 0) {
        if (k & 1) res = multiply(res, A, mod);
        A = multiply(A, A, mod);
        k >>= 1;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int d;
    long long k, mod;
    if (!(cin >> d >> k >> mod)) return 0;

    Matrix A(d, vector<long long>(d));
    for (int i = 0; i < d; i++) {
        for (int j = 0; j < d; j++) {
            cin >> A[i][j];
            A[i][j] %= mod;
        }
    }

    Matrix ans = matrix_pow(A, k, mod);

    for (int i = 0; i < d; i++) {
        for (int j = 0; j < d; j++) {
            cout << ans[i][j] << (j + 1 == d ? "" : " ");
        }
        cout << "\\n";
    }

    return 0;
}
"""


def _generate_combinatorics_factorials() -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

// Extended GCD
long long ext_gcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) {
        if (a >= 0) { x = 1; y = 0; return a; }
        else { x = -1; y = 0; return -a; }
    }
    long long x1, y1;
    long long g = ext_gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

long long mod_inverse(long long a, long long m) {
    long long x, y;
    ext_gcd(a, m, x, y);
    return (x % m + m) % m;
}

const int MAXN = 1000000;
long long fact[MAXN + 1];
long long invFact[MAXN + 1];

void precompute_factorials(int n, long long p) {
    fact[0] = 1;
    for (int i = 1; i <= n; i++) {
        fact[i] = ((__int128_t)fact[i - 1] * i) % p;
    }
    invFact[n] = mod_inverse(fact[n], p);
    for (int i = n - 1; i >= 0; i--) {
        invFact[i] = ((__int128_t)invFact[i + 1] * (i + 1)) % p;
    }
}

long long nCr(int n, int k, long long p) {
    if (k < 0 || k > n) return 0;
    return ((__int128_t)fact[n] * invFact[k] % p * invFact[n - k]) % p;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    long long p;
    if (!(cin >> n >> k >> p)) return 0;

    // Gate E: ordinary factorial precomputation requires N < p
    if (n >= p) {
        cout << "INVALID_PRECONDITION_N_GE_P\\n";
        return 0;
    }

    precompute_factorials(n, p);
    cout << nCr(n, k, p) << "\\n";

    return 0;
}
"""


def _generate_lucas_theorem() -> str:
    return """#include <iostream>
#include <vector>

using namespace std;

// Power modulo
long long power_mod(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = ((__int128_t)res * base) % mod;
        base = ((__int128_t)base * base) % mod;
        exp >>= 1;
    }
    return res;
}

long long mod_inverse_prime(long long a, long long p) {
    return power_mod(a, p - 2, p);
}

// Small nCr mod p using direct calculation
long long small_nCr(long long n, long long k, long long p) {
    if (k < 0 || k > n) return 0;
    if (k == 0 || k == n) return 1;
    long long num = 1, den = 1;
    for (long long i = 1; i <= k; i++) {
        num = ((__int128_t)num * (n - i + 1)) % p;
        den = ((__int128_t)den * i) % p;
    }
    return ((__int128_t)num * mod_inverse_prime(den, p)) % p;
}

// Lucas' Theorem for arbitrary n, k >= 0 and prime p
long long lucas(long long n, long long k, long long p) {
    if (k < 0 || k > n) return 0;
    long long ans = 1;
    while (n > 0 || k > 0) {
        long long ni = n % p;
        long long ki = k % p;
        if (ki > ni) return 0;
        ans = ((__int128_t)ans * small_nCr(ni, ki, p)) % p;
        n /= p;
        k /= p;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, k, p;
    if (!(cin >> n >> k >> p)) return 0;

    cout << lucas(n, k, p) << "\\n";
    return 0;
}
"""


def _generate_miller_rabin() -> str:
    return """#include <iostream>

using namespace std;

// Safe modular multiplication using unsigned 128-bit integer
unsigned long long mul_mod(unsigned long long a, unsigned long long b, unsigned long long m) {
    return (unsigned long long)(((__uint128_t)a * b) % m);
}

// Binary exponentiation for unsigned 64-bit integers
unsigned long long power_mod(unsigned long long base, unsigned long long exp, unsigned long long mod) {
    unsigned long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = mul_mod(res, base, mod);
        base = mul_mod(base, base, mod);
        exp >>= 1;
    }
    return res;
}

// Deterministic Miller-Rabin Primality Test for all N < 2^64
// Uses locked 7-witness basis: {2, 325, 9375, 28178, 450775, 9780504, 1795265022}
bool is_prime_64(unsigned long long n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    unsigned long long d = n - 1;
    int s = 0;
    while (d % 2 == 0) {
        d /= 2;
        s++;
    }

    const unsigned long long witnesses[7] = {
        2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL
    };

    for (unsigned long long a : witnesses) {
        if (a % n == 0) continue;
        unsigned long long x = power_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;

        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    unsigned long long n;
    if (!(cin >> n)) return 0;

    if (is_prime_64(n)) {
        cout << "PRIME\\n";
    } else {
        cout << "COMPOSITE\\n";
    }

    return 0;
}
"""
