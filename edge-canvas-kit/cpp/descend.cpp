// descend.cpp -- C++ twin of lib/descend.py (Timothy's descending forward-difference update).
// f(x) = m*x^n + B. Build the forward-difference table at x0 with step dx, walk it `steps`
// times by additions only, print the FINAL value only. Exact rationals: integer numerator and
// denominator (long long), normalized by gcd, every multiply/add overflow-checked.
// Fail closed: on overflow or walk != closed form the program prints REFUSED, never a guess.
// Locked case 2026-10-05: m=5, n=3, B=7, x0=0, dx=3, steps=4 -> 8647.
// Build: g++ -std=c++17 -O1 -o descend descend.cpp   Run: ./descend
#include <iostream>
#include <string>
#include <vector>
#include <numeric>
#include <climits>
#include <stdexcept>

struct Q {                       // exact rational num/den, den > 0, gcd(num, den) = 1
    long long n, d;
};

static long long chk_mul(long long a, long long b) {
    if (a == 0 || b == 0) return 0;
    if (a == LLONG_MIN || b == LLONG_MIN) throw std::overflow_error("mul");
    long long aa = a < 0 ? -a : a, bb = b < 0 ? -b : b;
    if (aa > LLONG_MAX / bb) throw std::overflow_error("mul");
    return a * b;
}
static long long chk_add(long long a, long long b) {
    if ((b > 0 && a > LLONG_MAX - b) || (b < 0 && a < LLONG_MIN - b)) throw std::overflow_error("add");
    return a + b;
}
static Q norm(long long n, long long d) {
    if (d == 0) throw std::domain_error("zero denominator");
    if (d < 0) { if (n == LLONG_MIN || d == LLONG_MIN) throw std::overflow_error("neg"); n = -n; d = -d; }
    long long g = std::gcd(n < 0 ? -n : n, d);
    if (g == 0) g = 1;
    return Q{n / g, d / g};
}
static Q add(Q a, Q b) {
    long long g = std::gcd(a.d, b.d);
    long long l = chk_mul(a.d / g, b.d);
    return norm(chk_add(chk_mul(a.n, l / a.d), chk_mul(b.n, l / b.d)), l);
}
static Q neg(Q a) { if (a.n == LLONG_MIN) throw std::overflow_error("neg"); return Q{-a.n, a.d}; }
static Q sub(Q a, Q b) { return add(a, neg(b)); }
static Q mul(Q a, Q b) {
    long long g1 = std::gcd(a.n < 0 ? -a.n : a.n, b.d), g2 = std::gcd(b.n < 0 ? -b.n : b.n, a.d);
    if (g1 == 0) g1 = 1;
    if (g2 == 0) g2 = 1;
    return norm(chk_mul(a.n / g1, b.n / g2), chk_mul(a.d / g2, b.d / g1));
}
static Q qi(long long v) { return Q{v, 1}; }
static Q pw(Q x, int n) { Q r = qi(1); for (int i = 0; i < n; ++i) r = mul(r, x); return r; }
static Q f_at(Q m, int n, Q B, Q x) { return add(mul(m, pw(x, n)), B); }
static bool eq(Q a, Q b) { return a.n == b.n && a.d == b.d; }
static std::string fmt(Q a) { return a.d == 1 ? std::to_string(a.n) : std::to_string(a.n) + "/" + std::to_string(a.d); }

// DESC_UPDATE: final value only. Throws on overflow or mismatch (fail closed).
static Q final_value(Q m, int n, Q B, Q x0, Q dx, long long steps) {
    if (n < 0 || n > 32 || steps < 0 || steps > 1000000) throw std::domain_error("range");
    std::vector<Q> row;
    for (int k = 0; k <= n; ++k) row.push_back(f_at(m, n, B, add(x0, mul(qi(k), dx))));
    std::vector<Q> d;
    for (int lvl = 0; lvl <= n; ++lvl) {
        d.push_back(row[0]);
        std::vector<Q> nx;
        for (size_t i = 0; i + 1 < row.size(); ++i) nx.push_back(sub(row[i + 1], row[i]));
        row = nx;
    }
    for (long long s = 0; s < steps; ++s)
        for (int k = 0; k < n; ++k) d[k] = add(d[k], d[k + 1]);
    Q closed = f_at(m, n, B, add(x0, mul(qi(steps), dx)));
    if (!eq(d[0], closed)) throw std::logic_error("walk != closed form");
    return d[0];
}

static std::string try_final(Q m, int n, Q B, Q x0, Q dx, long long steps) {
    try { return fmt(final_value(m, n, B, x0, dx, steps)); }
    catch (const std::exception&) { return "REFUSED"; }
}

int main() {
    std::cout << try_final(qi(5), 3, qi(7), qi(0), qi(3), 4) << "\n";   // locked case: final only
    int pass = 0, fail = 0;
    auto t = [&](const std::string& name, bool ok) { std::cout << (ok ? "PASS: " : "FAIL: ") << name << "\n"; ok ? ++pass : ++fail; };
    t("locked_5x3p7_dx3_4steps_8647", try_final(qi(5), 3, qi(7), qi(0), qi(3), 4) == "8647");
    t("hundredths_dx_1/100_3steps", try_final(qi(5), 3, qi(7), qi(0), Q{1, 100}, 3) == "1400027/200000");
    t("zero_steps_is_f_x0", try_final(qi(5), 3, qi(7), qi(0), qi(3), 0) == "7");
    t("one_step_142", try_final(qi(5), 3, qi(7), qi(0), qi(3), 1) == "142");
    t("three_steps_3652", try_final(qi(5), 3, qi(7), qi(0), qi(3), 3) == "3652");
    t("n0_constant", try_final(qi(5), 0, qi(7), qi(0), qi(3), 4) == "12");
    t("negative_dx", try_final(qi(5), 3, qi(7), qi(0), qi(-3), 4) == "-8633");
    t("half_m_half_dx", try_final(Q{1, 2}, 2, qi(0), qi(0), Q{1, 2}, 2) == "1/2");
    t("norm_2/4_is_1/2", fmt(norm(2, 4)) == "1/2");
    t("norm_sign_1/-2", fmt(norm(1, -2)) == "-1/2");
    t("overflow_refused", try_final(qi(1000000), 5, qi(0), qi(0), qi(1000000), 3) == "REFUSED");
    t("range_refused_n33", try_final(qi(1), 33, qi(0), qi(0), qi(1), 1) == "REFUSED");
    t("range_refused_neg_steps", try_final(qi(1), 1, qi(0), qi(0), qi(1), -1) == "REFUSED");
    bool mo = false, ao = false;
    try { chk_mul(LLONG_MAX / 2 + 1, 2); } catch (const std::overflow_error&) { mo = true; }
    try { chk_add(LLONG_MAX, 1); } catch (const std::overflow_error&) { ao = true; }
    t("mul_overflow_detected", mo);
    t("add_overflow_detected", ao);
    std::cout << "PASS=" << pass << " FAIL=" << fail << "\n";
    std::cout << (fail == 0 ? "SUMMARY: ALL PASS" : "SUMMARY: FAILS") << "\n";
    return fail == 0 ? 0 : 1;
}
