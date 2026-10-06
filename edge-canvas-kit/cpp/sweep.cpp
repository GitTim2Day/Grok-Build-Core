// sweep.cpp -- C++ twin of lib/sweep.py key values (Spectrum Sweep, 2026-10-06).
// Mapping f = 130.8 * 2^y Hz  ->  y = log2(f / 130.8).  Redshift f_obs = f / (1 + z): a shift of log2(1+z) octaves.
// Values are cut (truncated) to 8 places, never rounded; exact powers of two give exact octaves.
// Colour: visible wavelength -> RGB (piecewise-linear, edge fall-off, gamma 0.8, channels truncated), as lib/sweep.py.
// Representation only: this program emits and detects nothing.
// Cross-check tolerance with Python and BASIC: 1e-7 on the 8-place values (long double here).
// Build: g++ -std=c++17 -O1 -o sweep sweep.cpp   Run: ./sweep
#include <iostream>
#include <string>
#include <cmath>
#include <array>

static int pass_n = 0, fail_n = 0;
static void check(const std::string& name, bool ok) {
    if (ok) ++pass_n; else { ++fail_n; std::cout << "FAIL " << name << "\n"; }
}

static long double ylog2(long double x) {          // exact when x is a power of two
    long double y = std::log2(x);
    long double r = std::floor(y + 0.5L);
    if (std::ldexp(1.0L, (int)r) == x) return r;
    return y;
}

static std::string cut8(long double v) {           // v >= 0, truncated to 8 places, zero-padded
    long long ip = (long long)std::floor(v);
    long long fp = (long long)std::floor((v - (long double)ip) * 100000000.0L);
    std::string f = std::to_string(fp);
    while (f.size() < 8) f = "0" + f;
    return std::to_string(ip) + "." + f;
}

static std::array<int, 3> wavelength_to_rgb(double nm) {
    double lam = nm < 380 ? 380 : (nm > 780 ? 780 : nm), r, g, b, fac;
    if (lam < 440) { r = (440 - lam) / (440 - 380); g = 0; b = 1; }
    else if (lam < 490) { r = 0; g = (lam - 440) / (490 - 440); b = 1; }
    else if (lam < 510) { r = 0; g = 1; b = (510 - lam) / (510 - 490); }
    else if (lam < 580) { r = (lam - 510) / (580 - 510); g = 1; b = 0; }
    else if (lam < 645) { r = 1; g = (645 - lam) / (645 - 580); b = 0; }
    else { r = 1; g = 0; b = 0; }
    if (lam < 420) fac = 0.3 + 0.7 * (lam - 380) / (420 - 380);
    else if (lam <= 700) fac = 1.0;
    else fac = 0.3 + 0.7 * (780 - lam) / (780 - 700);
    std::array<double, 3> c{r, g, b};
    std::array<int, 3> o{0, 0, 0};
    for (int i = 0; i < 3; ++i) o[i] = c[i] > 0 ? (int)(255 * std::pow(c[i] * fac, 0.8)) : 0;
    return o;
}

int main() {
    const long double F0 = 130.8L;
    long double y100 = ylog2(100000000.0L / F0), y500 = ylog2(500000000000000.0L / F0);
    std::string k1 = cut8(y100), k5 = cut8(y500);
    std::string s1 = cut8(ylog2(2.0L)), s3 = cut8(ylog2(4.0L)), sh = cut8(ylog2(1.5L));
    std::cout << "Y100 " << k1 << "\n" << "Y500 " << k5 << "\n";
    std::cout << "SHIFT_Z1 " << s1 << "\nSHIFT_Z3 " << s3 << "\nSHIFT_ZHALF " << sh << "\n";
    // descending fixed-step sampler: y = 42 - x/4, x = 0..90, additions only; print the final value only
    long double ys = 42.0L;
    for (int i = 0; i < 90; ++i) ys += -0.25L;
    std::cout << "SAMPLER_FINAL " << cut8(ys) << "\n";
    // self-checks
    check("f_at_y100_is_100MHz", std::fabs(F0 * std::pow(2.0L, y100) - 1e8L) / 1e8L < 1e-15L);
    check("y500_minus_y100", std::fabs((y500 - y100) - std::log2(5000000.0L)) < 1e-12L);
    check("y100_trunc8", k1 == "19.54420602");
    check("y500_trunc8", k5 == "41.79770269");
    check("shift_z1", s1 == "1.00000000");
    check("shift_z3", s3 == "2.00000000");
    check("shift_zhalf", sh == "0.58496250");
    check("sampler_final_19.5", ys == 19.5L && ys == 42.0L - 90 * 0.25L);
    long double fo = 500000000000000.0L / (1 + 1);
    check("redshift_divides", fo < 500000000000000.0L && std::fabs(ylog2(fo / F0) - (y500 - 1)) < 1e-12L);
    long double l1 = 299792458.0L / 400e12L * 1e9L, l2 = 299792458.0L / 790e12L * 1e9L;
    check("visible_400_790THz_in_nm", l1 > 749 && l1 < 750 && l2 > 379 && l2 < 380);
    auto eq = [](std::array<int, 3> a, int r, int g, int b) { return a[0] == r && a[1] == g && a[2] == b; };
    check("rgb_440_blue", eq(wavelength_to_rgb(440), 0, 0, 255));
    check("rgb_490_cyan", eq(wavelength_to_rgb(490), 0, 255, 255));
    check("rgb_510_green", eq(wavelength_to_rgb(510), 0, 255, 0));
    check("rgb_580_yellow", eq(wavelength_to_rgb(580), 255, 255, 0));
    check("rgb_645_red", eq(wavelength_to_rgb(645), 255, 0, 0));
    std::array<int, 3> v380 = wavelength_to_rgb(380), v780 = wavelength_to_rgb(780);
    std::cout << "RGB380 " << v380[0] << "," << v380[1] << "," << v380[2] << "\n";
    std::cout << "RGB780 " << v780[0] << "," << v780[1] << "," << v780[2] << "\n";
    std::cout << "PASS=" << pass_n << " FAIL=" << fail_n << "\n";
    std::cout << (fail_n == 0 ? "SUMMARY: ALL PASS" : "SUMMARY: FAILS") << "\n";
    return fail_n == 0 ? 0 : 1;
}
