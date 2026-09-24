// Preferred path: embed the two ends. Average is archived.
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct R {
    std::int64_t n;
    std::int64_t d;
    bool operator==(const R& o) const { return n == o.n && d == o.d; }
    bool operator<(const R& o) const { return n * o.d < o.n * d; }
};

static R add(R a, R b) {
    return R{a.n * b.d + b.n * a.d, a.d * b.d};
}
static R half_mean_trunc8(R a, R b) {
    if (a.n < 0 || b.n < 0) throw std::runtime_error("magnitude must be positive");
    __int128 num = (__int128)a.n * b.d + (__int128)b.n * a.d;
    __int128 den = (__int128)a.d * b.d * 2;
    __int128 scaled = num * 100000000 / den;
    return R{static_cast<std::int64_t>(scaled), 100000000};
}

struct Pack {
    R face[6][6];
    R col0[8];
    R col7[8];
    R row0[6];
    R row7[6];
};

static void embed_axis(const R in[8], R face[6], R& end0, R& end7) {
    for (int i = 0; i < 8; ++i) {
        if (in[i].n < 0 || in[i].d <= 0) throw std::runtime_error("magnitude must be positive");
    }
    end0 = in[0];
    end7 = in[7];
    for (int i = 0; i < 6; ++i) face[i] = in[i + 1];
}

static Pack embed_grid(const R g[8][8]) {
    Pack p{};
    R mid[8][6];
    for (int r = 0; r < 8; ++r) {
        embed_axis(g[r], mid[r], p.col0[r], p.col7[r]);
    }
    for (int c = 0; c < 6; ++c) p.row0[c] = mid[0][c];
    for (int c = 0; c < 6; ++c) p.row7[c] = mid[7][c];
    for (int r = 0; r < 6; ++r)
        for (int c = 0; c < 6; ++c)
            p.face[r][c] = mid[r + 1][c];
    return p;
}

static void restore(const Pack& p, R out[8][8]) {
    for (int r = 0; r < 8; ++r) {
        out[r][0] = p.col0[r];
        out[r][7] = p.col7[r];
    }
    for (int c = 0; c < 6; ++c) {
        out[0][c + 1] = p.row0[c];
        out[7][c + 1] = p.row7[c];
    }
    for (int r = 0; r < 6; ++r)
        for (int c = 0; c < 6; ++c)
            out[r + 1][c + 1] = p.face[r][c];
}

static void average_axis(const R in[8], R out[6]) {
    R a[7];
    for (int i = 0; i < 7; ++i) a[i] = half_mean_trunc8(in[i], in[i + 1]);
    for (int i = 0; i < 6; ++i) out[i] = half_mean_trunc8(a[i], a[i + 1]);
}

int main() {
    const R base[8] = {
        {1, 3}, {1, 7}, {1, 9}, {5, 11}, {1, 13}, {2, 5}, {1, 17}, {3, 8},
    };
    R grid[8][8];
    for (int r = 0; r < 8; ++r) {
        for (int c = 0; c < 8; ++c) {
            R b = base[(c + r) % 8];
            grid[r][c] = add(b, R{r, 64});
        }
    }
    grid[3][3] = R{1000, 1};
    Pack pack = embed_grid(grid);
    R back[8][8];
    restore(pack, back);
    int mismatch = 0;
    for (int r = 0; r < 8; ++r)
        for (int c = 0; c < 8; ++c)
            if (!(back[r][c] == grid[r][c])) ++mismatch;
    bool quirk = pack.face[2][2] == R{1000, 1};
    R blended[6];
    average_axis(grid[3], blended);
    bool smear = !(blended[0] == R{1000, 1});
    int failed = 0;
    try {
        R bad[8];
        for (int i = 0; i < 8; ++i) bad[i] = R{1, 1};
        bad[0] = R{-1, 1};
        R f[6]; R a, b;
        embed_axis(bad, f, a, b);
        std::cout << "SIGNED_NOT_REJECTED\n";
        failed = 1;
    } catch (const std::runtime_error&) {
        std::cout << "SIGNED_REJECTED\n";
    }
    std::cout << "EMBED_MISMATCH " << mismatch << "\n";
    std::cout << "QUIRK_ON_FACE " << (quirk ? "1000" : "LOST") << "\n";
    std::cout << "FACE 6 6\n";
    std::cout << "ARCHIVED_SMEARED " << (smear ? "YES" : "NO") << "\n";
    if (mismatch != 0 || !quirk || !smear) failed = 1;
    std::cout << "STATUS " << (failed ? "FAIL" : "ALL_GREEN") << "\n";
    return failed;
}
