// cut8.cpp v2 -- C++ twin of cut8.bas (Tim's rules 2026-10-08). Same steps, same limit.
#include <cmath>
#include <cstdio>
#include <string>
static const double LM = 99999.0;
std::string cut8(double v) {
    if (v == 0.0) v = 0.0;                          // -0 and 0 -> 0
    int s = (v < 0.0) ? -1 : 1;                     // sign is a direction
    double m = v * s;                               // positive magnitude
    double p = std::floor(m);                       // reduce: integer part first
    if (p > LM) return "REFUSED";
    double w = std::floor((m - p) * 1e10 + 0.5);    // round fraction once at 10 places
    if (w >= 1e10) { p += 1.0; w -= 1e10; }         // carry
    double q = std::floor(w / 100.0);               // cut to 8 places
    char buf[64];
    std::snprintf(buf, sizeof buf, "%.0f.%08.0f", p, q);
    std::string t(buf);
    if (s < 0 && (p > 0.0 || q > 0.0)) t = "-" + t; // no negative zero
    return t;
}
int main() {
    struct C { const char* k; double v; } cs[] = {
        {"Y100", std::log(100000000/130.8)/std::log(2.0)}, {"Y500", std::log(500000000000000/130.8)/std::log(2.0)},
        {"Z1", 1.0}, {"Z3", 2.0}, {"ZHALF", std::log(1.5)/std::log(2.0)}, {"SAMPLER", 19.5},
        {"ZERO", 0.0}, {"NEGZERO", -0.0}, {"NEG", -0.58496250072}, {"TINYNEG", -0.000000001},
        {"NINES", 0.999999999}, {"NOISE", 0.1+0.2}, {"BIG", 12345678.87654321}, {"ONE_ULP_UNDER", 2.9999999999999996},
        {"CARRY", 0.99999999999}, {"NEGCARRY", -4.99999999999}, {"HUGE", 1e16}, {"EDGE5", 99999.12345678}, {"OVER5", 100000.5}};
    for (auto& c : cs) std::printf("%s %s\n", c.k, cut8(c.v).c_str());
}
