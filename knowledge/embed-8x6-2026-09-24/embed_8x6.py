"""Preferred path: embed the two ends. Average is archived."""
from fractions import Fraction

SCALE = 10**8


def trunc8(x: Fraction) -> Fraction:
    if x < 0:
        raise ValueError("truncate the positive magnitude, not a signed value")
    return Fraction(int(x * SCALE), SCALE)


def embed_axis(line):
    if len(line) != 8:
        raise ValueError("axis must be 8")
    for v in line:
        if v < 0:
            raise ValueError("magnitude must be positive")
    return list(line[1:7]), line[0], line[7]


def embed_grid(grid):
    if len(grid) != 8 or any(len(row) != 8 for row in grid):
        raise ValueError("grid must be 8 by 8")
    face86 = []
    col0, col7 = [], []
    for row in grid:
        face, a, b = embed_axis(row)
        face86.append(face)
        col0.append(a)
        col7.append(b)
    face66 = [row[:] for row in face86[1:7]]
    return {
        "face": face66,
        "embed": {
            "col0": col0,
            "col7": col7,
            "row0": list(face86[0]),
            "row7": list(face86[7]),
        },
    }


def restore(pack):
    e = pack["embed"]
    full = [[None] * 8 for _ in range(8)]
    for r in range(8):
        full[r][0] = e["col0"][r]
        full[r][7] = e["col7"][r]
    for c in range(6):
        full[0][c + 1] = e["row0"][c]
        full[7][c + 1] = e["row7"][c]
    for r in range(6):
        for c in range(6):
            full[r + 1][c + 1] = pack["face"][r][c]
    return full


def average_axis(line):
    """Archived. Not the memory. Sliding pair, twice. Truncate toward zero."""
    if len(line) != 8:
        raise ValueError("axis must be 8")

    def once(xs):
        out = []
        for a, b in zip(xs, xs[1:]):
            if a < 0 or b < 0:
                raise ValueError("magnitude must be positive")
            out.append(trunc8((a + b) / 2))
        return out

    return once(once(line))


def _sample():
    base = [
        Fraction(1, 3), Fraction(1, 7), Fraction(1, 9), Fraction(5, 11),
        Fraction(1, 13), Fraction(2, 5), Fraction(1, 17), Fraction(3, 8),
    ]
    grid = []
    for r in range(8):
        grid.append([base[(c + r) % 8] + Fraction(r, 64) for c in range(8)])
    grid[3][3] = Fraction(1000)
    return grid


def basic_average_axis(line):
    """Same rule as BASIC backslash. Archived. Not the memory."""
    if len(line) != 8:
        raise ValueError("axis must be 8")
    once = []
    for a, b in zip(line, line[1:]):
        if a < 0 or b < 0:
            raise ValueError("magnitude must be positive")
        once.append((a + b) // 2)
    return [(a + b) // 2 for a, b in zip(once, once[1:])]


def basic_integer_trial():
    """The BASIC sample: ones, quirk 1000 at 1-based (4,4)."""
    grid = [[1] * 8 for _ in range(8)]
    grid[3][3] = 1000
    pack = embed_grid(grid)
    back = restore(pack)
    mismatch = sum(back[r][c] != grid[r][c] for r in range(8) for c in range(8))
    peak = max(basic_average_axis(grid[3]))
    print("BASIC_QUIRK_ON_FACE", pack["face"][2][2])
    print("BASIC_EMBED_MISMATCH", mismatch)
    print("BASIC_ARCHIVED_ROW_PEAK", peak)
    ok = pack["face"][2][2] == 1000 and mismatch == 0 and peak == 500
    print("BASIC_MATCH", "ALL_GREEN" if ok else "FAIL")
    return 0 if ok else 1


def main():
    grid = _sample()
    pack = embed_grid(grid)
    back = restore(pack)
    mismatch = sum(back[r][c] != grid[r][c] for r in range(8) for c in range(8))
    quirk = pack["face"][2][2]
    blended = average_axis(grid[3])
    print("EMBED_MISMATCH", mismatch)
    print("QUIRK_ON_FACE", quirk)
    print("FACE", len(pack["face"]), len(pack["face"][0]))
    print("EMBED_LINES", 4)
    print("ARCHIVED_ROW_PEAK", max(blended))
    failed = 0
    try:
        embed_axis([Fraction(-1), *([Fraction(1)] * 7)])
    except ValueError:
        print("SIGNED_REJECTED")
    else:
        failed = 1
        print("SIGNED_NOT_REJECTED")
    if mismatch != 0 or quirk != 1000 or max(blended) == 1000:
        failed = 1
    if basic_integer_trial() != 0:
        failed = 1
    print("STATUS", "ALL_GREEN" if failed == 0 else "FAIL")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
