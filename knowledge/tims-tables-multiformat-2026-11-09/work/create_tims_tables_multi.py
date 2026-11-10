#!/usr/bin/env python3
"""
Tim's Tables — multi-format SVCT Edge Lookup builder
Produces the same logical tables as create_tims_tables_xlsx.py to:
  .xlsx .ods per-sheet .csv .txt (TSV) .json .jsonl

Rules (first-principles-tim / exact-ratio-loops / ratios-are-values):
  - Truncate never round
  - Store exact ratios (Fraction / ratio strings); decimals are renderings only
  - No stored zero; no ±∞ → UNDEFINED
  - No float stored as the value (text columns for ratios + truncated decimals)

csv/txt/json/jsonl: pure stdlib (Pi 5 ARM64 OK with no pip).
xlsx needs openpyxl; ods needs odfpy. Missing deps → skip that format with a note.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from decimal import Decimal, getcontext, ROUND_DOWN
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

getcontext().prec = 64
getcontext().rounding = ROUND_DOWN

UNDEFINED = "UNDEFINED"
VERSION = "multi-v1.0-2026-11-09"
ANCHOR_TS = "2026-11-09T20:20:00-05:00"  # America/New_York original-timestamp anchor


# ---------- exact helpers ----------

def trunc_dec(d: Decimal, places: int) -> str:
    """Truncate Decimal toward zero to `places` fractional digits. Never round."""
    if places < 0:
        raise ValueError("places must be >= 0")
    sign = Decimal("-1") if d < 0 else Decimal("1")
    ad = abs(d)
    scale = Decimal(10) ** places
    cut = (ad * scale).to_integral_value(rounding=ROUND_DOWN) / scale
    out = sign * cut
    # Fixed fractional width for stable Sheets import (text)
    if places == 0:
        return format(int(out), "d") if out == out.to_integral_value() else str(out)
    # Build truncated string without scientific notation
    as_int = int((ad * scale).to_integral_value(rounding=ROUND_DOWN))
    whole = as_int // (10 ** places)
    frac = as_int % (10 ** places)
    body = f"{whole}.{frac:0{places}d}"
    return ("-" + body) if sign < 0 else body


def ratio_str(f: Fraction) -> str:
    f = Fraction(f).limit_denominator()
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def render_ratio(f: Fraction, places: int) -> str:
    """Exact ratio → truncated decimal rendering (string). Zero → UNDEFINED."""
    f = Fraction(f)
    if f.numerator == 0:
        return UNDEFINED
    d = Decimal(f.numerator) / Decimal(f.denominator)
    return trunc_dec(d, places)


def from_high_dec(s: str, places: int) -> str:
    """Truncate a high-precision decimal string. Never round."""
    d = Decimal(s)
    if d == 0:
        return UNDEFINED
    return trunc_dec(d, places)


# High-precision constants via Decimal (no float path into storage)
# √2, √3 from Decimal.sqrt
_SQRT2 = Decimal(2).sqrt()
_SQRT3 = Decimal(3).sqrt()
_PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944")

# Precomputed irrational truncations used by tables
SIN45 = _SQRT2 / 2          # √2/2
COS45 = _SQRT2 / 2
SIN60 = _SQRT3 / 2          # √3/2
COS60 = Decimal("1") / 2
TAN60 = _SQRT3
# 2^(1/8), 2^(1/6), 2^(1/4), 2^(1/2), 2^(3/4)
# Use Decimal.exp/ln for roots: a^(p/q) = exp(p/q * ln a)
def _pow_trunc(base: Decimal, exp: Fraction, places: int) -> str:
    # base^(p/q) via Decimal ln/exp; exact integer when result is integral
    p, q = exp.numerator, exp.denominator
    if base <= 0:
        return UNDEFINED
    if exp == 0:
        return "1"  # x^0 = 1 identity
    if exp == 1:
        # base^1 = base; if integer, exact
        if base == base.to_integral_value():
            return str(int(base))
        return trunc_dec(base, places)
    val = (base.ln() * Decimal(p) / Decimal(q)).exp()
    if val == 0:
        return UNDEFINED
    # Detect near-exact integers (within 10^-(places+4)) and emit exact
    nearest = val.to_integral_value(rounding=ROUND_DOWN)
    # also check round-half — but we never round; only accept if trunc equals ceil within tiny eps via difference
    up = nearest + 1
    # if val is extremely close to an integer from below after high prec, still truncate
    # Prefer exact when Fraction power of integer base yields integer (e.g. 8^(1/3)=2) —
    # not in current spoke set, but keep integer emission when trunc_dec would be N.000000
    t = trunc_dec(val, places)
    if "." in t:
        whole, frac = t.split(".", 1)
        if frac == ("0" * places) and not t.startswith("-"):
            return whole if whole != "0" else UNDEFINED
        if frac == ("0" * places) and t.startswith("-"):
            return whole if whole != "-0" else UNDEFINED
    return t


def _log2_ratio(f: Fraction, places: int) -> str:
    """log2(f) truncated. Exact when f is power of 2."""
    if f.numerator == 0:
        return UNDEFINED
    # exact for pure powers of 2
    # 1/8 → -3, 1/4 → -2, 1/2 → -1, 1 → 0 (x^0 identity / log2(1)=0 → UNDEFINED per no-stored-zero)
    if f == Fraction(1, 8):
        return "-3"
    if f == Fraction(1, 4):
        return "-2"
    if f == Fraction(1, 2):
        return "-1"
    if f == Fraction(1, 1):
        return UNDEFINED  # log2(1)=0 → no stored zero
    # otherwise Decimal
    val = (Decimal(f.numerator) / Decimal(f.denominator)).ln() / Decimal(2).ln()
    if val == 0:
        return UNDEFINED
    return trunc_dec(val, places)


# ---------- table builders (shared data model) ----------
# Each sheet: {"name": str, "headers": [...], "rows": [[cell,...], ...]}
# Every numeric cell is a STRING (ratio or truncated decimal or UNDEFINED).

Sheet = Dict[str, Any]


def build_readme() -> Sheet:
    rows = [
        ["TIM'S TABLES — SVCT EDGE LOOKUP " + VERSION],
        [""],
        ["PURPOSE"],
        ["Fast O(1) lookup tables for the base-8 contact points (6 spokes + 2 poles for nuance). "
         "Pre-truncated values eliminate runtime irrational numbers (sqrt, pi, etc.) for edge "
         "computing acceleration in SVCT / KBLD workloads."],
        [""],
        ["LOCKED INVARIANTS (never change)"],
        ["• Base 8 contact points are INVARIANT — always free to bloom and procreate. Never reduce below 8."],
        ["• Exactly 2 extra poles exist ONLY for nuance the standard token cannot carry "
         "(original timestamp anchor first, then source/GPS/residual chord/coherence)."],
        ["• Truncation is mandatory. Interpolation introduces cumulative drift — avoided for "
         "long-running edge/SVCT stability."],
        ["• Precision tiers: e-6 (day-to-day), e-8 (physics/atmospheric), e-15 (cosmology/space nav). "
         "QM/protein cases stay symbolic or routed to free pole cells."],
        ["• All storage is four-pillar JSONL (content · context · data · time). "
         "Original timestamp anchor always in first free pole cell."],
        ["• No wormholes. No singularities. Finite. Musical. Bounded resonance only."],
        ["• Ratios are the values; decimals are renderings only. Truncate never round. "
         "No stored zero. No ±∞ (use UNDEFINED)."],
        [""],
        ["HOW TO USE FOR EDGE ACCELERATION"],
        ["1. Go to Core_Six_Ratios or All_Matrix_e6 sheet / CSV."],
        ["2. Copy the Ratio_* and Trunc_* columns into const arrays or dicts "
         "(no math.sin, no math.sqrt at runtime)."],
        ["3. Use Lookup_Dashboard for interactive bidirectional search "
         "(xlsx/ods dropdown; CSV: filter Spoke_Fraction)."],
        ["4. For PivotTables: Master_Flat_Data → Insert → PivotTable (Excel) or Data → Pivot (Sheets/LibreOffice)."],
        ["5. When spoke count scales later (9/81 → 360/360²), the same base-8 seeds bloom new cells."],
        [""],
        ["CURRENT COVERAGE"],
        ["Core 6 spokes (1/8, 1/6, 1/4, 1/2, 3/4, 1) + Trig + Reciprocals + Powers + "
         "Historical ratios + Navigation basics."],
        ["EM (UV→IR, redshift) and atmospheric sound extensions are latent and can be added "
         "on request without changing the header structure."],
        [""],
        ["ORIGINAL TIMESTAMP ANCHOR"],
        [ANCHOR_TS],
        [""],
        ["FILE READY FOR EDGE USE"],
        ["All values pre-truncated. No sqrt, pi, or irrational functions executed at runtime. "
         "Copy columns into const arrays for maximum speed on Pi 5 / Orin / edge devices."],
        ["When adding new categories (EM redshift, atmospheric sound, scaled music), append rows "
         "to Master_Flat_Data and extend the matrix sheets. Base-8 spokes remain the invariant bloom seeds."],
        ["Formats: xlsx (Excel), ods (LibreOffice), csv (Sheets-import), txt (TSV offline AI), "
         "json / jsonl (four-pillar edge)."],
    ]
    return {"name": "README_Instructions", "headers": ["Text"], "rows": [[r[0]] for r in rows]}


def build_core_six() -> Sheet:
    # Radians exact as k*pi ratio string; trunc e-15 of k*pi
    spokes = [
        # id, frac, deg, k_pi (Fraction of pi), exact_dec Fraction, notes
        (1, "1/8", "45", Fraction(1, 4), Fraction(1, 8),
         "Base-8 seed. Free to bloom. Original timestamp anchor in Pole 1."),
        (2, "1/6", "60", Fraction(1, 3), Fraction(1, 6),
         "Sexagesimal / clock / 60° sector. Free to bloom."),
        (3, "1/4", "90", Fraction(1, 2), Fraction(1, 4),
         "Right angle. Pole-adjacent. Free to bloom."),
        (4, "1/2", "180", Fraction(1, 1), Fraction(1, 2),
         "Opposite. Free to bloom. Residual chord reference."),
        (5, "3/4", "270", Fraction(3, 2), Fraction(3, 4),
         "Pole-adjacent. Free to bloom."),
        (6, "1", "360", Fraction(2, 1), Fraction(1, 1),
         "Full cycle / closure. Free to bloom. 2.08 Hz residual anchor point."),
    ]
    headers = [
        "Spoke_ID", "Fraction", "Degrees",
        "Radians_Ratio_of_pi", "Radians_Trunc_e15",
        "Exact_Ratio", "Trunc_Decimal_e15",
        "Notes_Nuance_in_2_Poles",
    ]
    rows = []
    for sid, frac, deg, k_pi, exact, notes in spokes:
        rad = _PI * Decimal(k_pi.numerator) / Decimal(k_pi.denominator)
        rows.append([
            str(sid),
            frac,
            deg,
            ratio_str(k_pi) + "*pi",
            trunc_dec(rad, 15),
            ratio_str(exact),
            render_ratio(exact, 15),
            notes,
        ])
    return {"name": "Core_Six_Ratios", "headers": headers, "rows": rows}


def build_trig_e6() -> Sheet:
    # Store Exact_Ratio (symbolic/ratio) + Trunc_e6 for sin/cos/tan; UNDEFINED for 0 and ∞
    # Direction: positive magnitudes; Direction column carries sign of original trig
    headers = [
        "Spoke_ID", "Fraction", "Angle_Deg",
        "Sin_Exact", "Sin_Trunc_e6", "Sin_Direction",
        "Cos_Exact", "Cos_Trunc_e6", "Cos_Direction",
        "Tan_Exact", "Tan_Trunc_e6", "Tan_Direction",
        "Notes",
    ]
    # direction: + / - / UNDEFINED
    data = [
        (1, "1/8", "45",
         "sqrt2/2", trunc_dec(SIN45, 6), "+",
         "sqrt2/2", trunc_dec(COS45, 6), "+",
         "1", "1", "+",
         "√2/2 exact. Truncated e-6."),
        (2, "1/6", "60",
         "sqrt3/2", trunc_dec(SIN60, 6), "+",
         "1/2", trunc_dec(COS60, 6), "+",
         "sqrt3", trunc_dec(TAN60, 6), "+",
         "√3/2, 1/2, √3. Truncated e-6."),
        (3, "1/4", "90",
         "1", "1", "+",
         UNDEFINED, UNDEFINED, UNDEFINED,  # cos(90)=0
         UNDEFINED, UNDEFINED, UNDEFINED,  # tan pole
         "Exact 1. Cos and Tan at pole → UNDEFINED (nuance in free pole cell)."),
        (4, "1/2", "180",
         UNDEFINED, UNDEFINED, UNDEFINED,  # sin(180)=0
         "1", "1", "-",             # cos = -1 → magnitude 1, direction -
         UNDEFINED, UNDEFINED, UNDEFINED,  # tan=0
         "Cos magnitude 1 opposite direction. Sin/Tan zero → UNDEFINED."),
        (5, "3/4", "270",
         "1", "1", "-",             # sin = -1
         UNDEFINED, UNDEFINED, UNDEFINED,  # cos=0
         UNDEFINED, UNDEFINED, UNDEFINED,  # tan pole
         "Sin magnitude 1 down. Cos/Tan at pole → UNDEFINED."),
        (6, "1", "360",
         UNDEFINED, UNDEFINED, UNDEFINED,  # sin=0
         "1", "1", "+",             # cos=1
         UNDEFINED, UNDEFINED, UNDEFINED,  # tan=0
         "Full cycle closure. Cos exact 1. Sin/Tan zero → UNDEFINED."),
    ]
    rows = [[str(x) for x in row] for row in data]
    return {"name": "Trig_e6", "headers": headers, "rows": rows}


def build_all_matrix_e6() -> Sheet:
    # Function rows × spoke columns; each value is Ratio or Trunc string
    spokes = [
        ("1/8", Fraction(1, 8)),
        ("1/6", Fraction(1, 6)),
        ("1/4", Fraction(1, 4)),
        ("1/2", Fraction(1, 2)),
        ("3/4", Fraction(3, 4)),
        ("1", Fraction(1, 1)),
    ]
    headers = [
        "Function",
        "1/8_45", "1/6_60", "1/4_90", "1/2_180", "3/4_270", "1_360",
        "Precision", "Category",
    ]

    def sin_at(frac: Fraction) -> str:
        mapping = {
            Fraction(1, 8): trunc_dec(SIN45, 6),
            Fraction(1, 6): trunc_dec(SIN60, 6),
            Fraction(1, 4): "1",
            Fraction(1, 2): UNDEFINED,
            Fraction(3, 4): "1",  # magnitude; direction in Notes/Trig sheet
            Fraction(1, 1): UNDEFINED,
        }
        return mapping[frac]

    def cos_at(frac: Fraction) -> str:
        mapping = {
            Fraction(1, 8): trunc_dec(COS45, 6),
            Fraction(1, 6): trunc_dec(COS60, 6),
            Fraction(1, 4): UNDEFINED,
            Fraction(1, 2): "1",
            Fraction(3, 4): UNDEFINED,
            Fraction(1, 1): "1",
        }
        return mapping[frac]

    def tan_at(frac: Fraction) -> str:
        mapping = {
            Fraction(1, 8): "1",
            Fraction(1, 6): trunc_dec(TAN60, 6),
            Fraction(1, 4): UNDEFINED,
            Fraction(1, 2): UNDEFINED,
            Fraction(3, 4): UNDEFINED,
            Fraction(1, 1): UNDEFINED,
        }
        return mapping[frac]

    def recip(frac: Fraction) -> str:
        if frac.numerator == 0:
            return UNDEFINED
        return ratio_str(1 / frac)

    def freq(frac: Fraction) -> str:
        return ratio_str(frac)

    def wave(frac: Fraction) -> str:
        return recip(frac)

    rows = [
        ["Sin"] + [sin_at(f) for _, f in spokes] + ["e-6", "Trig"],
        ["Cos"] + [cos_at(f) for _, f in spokes] + ["e-6", "Trig"],
        ["Tan"] + [tan_at(f) for _, f in spokes] + ["e-6", "Trig"],
        ["1/x_Reciprocal"] + [recip(f) for _, f in spokes] + ["e-6", "Reciprocal"],
        ["2^x_Power"] + [_pow_trunc(Decimal(2), f, 6) for _, f in spokes] + ["e-6", "Power"],
        ["6^x_Base-6"] + [_pow_trunc(Decimal(6), f, 6) for _, f in spokes] + ["e-6", "Power"],
        ["8^x_Base-8"] + [_pow_trunc(Decimal(8), f, 6) for _, f in spokes] + ["e-6", "Power"],
        ["log2_x"] + [_log2_ratio(f, 6) for _, f in spokes] + ["e-6", "Log"],
        ["Frequency_Ratio"] + [freq(f) for _, f in spokes] + ["e-6", "Physics"],
        ["Wavelength_Ratio_1_over_f"] + [wave(f) for _, f in spokes] + ["e-6", "Physics"],
    ]
    return {"name": "All_Matrix_e6", "headers": headers, "rows": rows}


def build_lookup_dashboard() -> Sheet:
    headers = ["Property", "Value_e6", "Value_e8", "Notes_Pole_Nuance"]
    # Default selected spoke = 1/8 (matches original yellow cell default)
    rows = [
        ["SELECT_SPOKE_DEFAULT", "1/8", "1/8", "Dropdown values: 1/8,1/6,1/4,1/2,3/4,1"],
        ["Fraction", "1/8", "1/8", "Base-8 seed cell"],
        ["Degrees", "45", "45", "45° spoke"],
        ["Sin", trunc_dec(SIN45, 6), trunc_dec(SIN45, 8), "Truncated. Exact √2/2"],
        ["Cos", trunc_dec(COS45, 6), trunc_dec(COS45, 8), "Truncated. Exact √2/2"],
        ["Tan", "1", "1", "Exact 1"],
        ["1/x_Reciprocal", "8", "8", "Exact integer"],
        ["2^x_Power", _pow_trunc(Decimal(2), Fraction(1, 8), 6),
         _pow_trunc(Decimal(2), Fraction(1, 8), 8), "Truncated"],
        ["Frequency_Ratio", "1/8", "1/8", "Exact 1/8"],
        ["REVERSE_LOOKUP_TIP", "", "",
         "To find which spoke a value belongs to (e.g. sin ≈ 0.866025), filter Trig_e6 "
         "Sin_Trunc_e6. All values are pre-truncated — no irrational computation at edge runtime."],
    ]
    return {"name": "Lookup_Dashboard", "headers": headers, "rows": rows}


def build_master_flat() -> Sheet:
    headers = [
        "Category", "Function", "Spoke_Fraction", "Spoke_Degrees",
        "Exact_Ratio_or_Symbolic", "Trunc_e6", "Trunc_e8", "Notes",
    ]
    rows = [
        ["Trig", "Sin", "1/8", "45", "sqrt2/2", trunc_dec(SIN45, 6), trunc_dec(SIN45, 8), "Base-8 seed"],
        ["Trig", "Sin", "1/6", "60", "sqrt3/2", trunc_dec(SIN60, 6), trunc_dec(SIN60, 8), "Sexagesimal"],
        ["Trig", "Sin", "1/4", "90", "1", "1", "1", "Pole-adjacent"],
        ["Trig", "Cos", "1/8", "45", "sqrt2/2", trunc_dec(COS45, 6), trunc_dec(COS45, 8), ""],
        ["Reciprocal", "1/x", "1/8", "45", "8", "8", "8", "Unit fraction friendly"],
        ["Power", "2^x", "1/8", "45", "2^(1/8)",
         _pow_trunc(Decimal(2), Fraction(1, 8), 6),
         _pow_trunc(Decimal(2), Fraction(1, 8), 8), "Bit scaling"],
        ["Physics", "Frequency_Ratio", "1/8", "45", "1/8", "1/8", "1/8", "E ∝ f"],
        ["Physics", "Wavelength_Ratio", "1/8", "45", "8", "8", "8", "λ ∝ 1/f"],
        ["Log", "log2(x)", "1/8", "45", "-3", "-3", "-3", "Bit shift"],
    ]
    return {"name": "Master_Flat_Data", "headers": headers, "rows": rows}


def build_all_sheets() -> List[Sheet]:
    return [
        build_readme(),
        build_core_six(),
        build_trig_e6(),
        build_all_matrix_e6(),
        build_lookup_dashboard(),
        build_master_flat(),
    ]


# ---------- writers ----------

def _assert_no_forbidden(sheets: List[Sheet]) -> List[str]:
    """Return list of violations: cell == '0' or float-looking rounded junk we can detect."""
    bad = []
    for sh in sheets:
        for r_i, row in enumerate(sh["rows"], start=2):
            for c_i, cell in enumerate(row, start=1):
                s = str(cell)
                if s == "0" or s == "0.0" or s == "0.000000" or s == "-0":
                    bad.append(f"{sh['name']}!R{r_i}C{c_i}={s!r}")
                if s in ("∞", "inf", "-inf", "Infinity", "-Infinity", "∞ (pole)"):
                    bad.append(f"{sh['name']}!R{r_i}C{c_i}={s!r}")
    return bad


def write_csv(sheets: List[Sheet], out_dir: Path) -> List[Path]:
    paths = []
    csv_dir = out_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    for sh in sheets:
        p = csv_dir / f"{sh['name']}.csv"
        with p.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(sh["headers"])
            for row in sh["rows"]:
                w.writerow([str(c) for c in row])
        paths.append(p)
    return paths


def write_txt(sheets: List[Sheet], out_dir: Path) -> List[Path]:
    """Tab-separated, offline-AI loadable."""
    paths = []
    txt_dir = out_dir / "txt"
    txt_dir.mkdir(parents=True, exist_ok=True)
    for sh in sheets:
        p = txt_dir / f"{sh['name']}.txt"
        with p.open("w", encoding="utf-8", newline="\n") as f:
            f.write("\t".join(str(h) for h in sh["headers"]) + "\n")
            for row in sh["rows"]:
                f.write("\t".join(str(c) for c in row) + "\n")
        paths.append(p)
    return paths


def write_json(sheets: List[Sheet], out_dir: Path) -> Path:
    p = out_dir / "Tims_Tables_SVCT_Edge_Lookup_v1.json"
    payload = {
        "title": "TIM'S TABLES — SVCT EDGE LOOKUP",
        "version": VERSION,
        "original_timestamp_anchor": ANCHOR_TS,
        "rules": [
            "truncate_never_round",
            "ratios_are_values",
            "no_stored_zero",
            "no_pm_infinity_use_UNDEFINED",
        ],
        "sheets": [
            {"name": sh["name"], "headers": sh["headers"], "rows": sh["rows"]}
            for sh in sheets
        ],
    }
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return p


def write_jsonl(sheets: List[Sheet], out_dir: Path) -> Path:
    """Four-pillar JSONL: content · context · data · time"""
    p = out_dir / "Tims_Tables_SVCT_Edge_Lookup_v1.jsonl"
    with p.open("w", encoding="utf-8") as f:
        # header record
        f.write(json.dumps({
            "content": "Tims_Tables_SVCT_Edge_Lookup",
            "context": "manifest",
            "data": {"version": VERSION, "sheet_count": len(sheets)},
            "time": ANCHOR_TS,
        }, ensure_ascii=False) + "\n")
        for sh in sheets:
            for r_i, row in enumerate(sh["rows"]):
                rec = {
                    "content": dict(zip(sh["headers"], [str(c) for c in row])),
                    "context": {"sheet": sh["name"], "row_index": r_i + 1},
                    "data": {"headers": sh["headers"]},
                    "time": ANCHOR_TS,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return p


def write_xlsx(sheets: List[Sheet], out_dir: Path) -> Path:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.worksheet.datavalidation import DataValidation
    except ImportError as e:
        raise RuntimeError(f"openpyxl required for xlsx: {e}") from e

    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill("solid", fgColor="1F4E79")
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin"),
    )
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    spoke_fill = PatternFill("solid", fgColor="D6DCE4")
    pole_fill = PatternFill("solid", fgColor="FFF2CC")
    e6_fill = PatternFill("solid", fgColor="E2EFDA")
    e8_fill = PatternFill("solid", fgColor="C6EFCE")

    wb = Workbook()
    first = True
    for sh in sheets:
        if first:
            ws = wb.active
            ws.title = sh["name"][:31]
            first = False
        else:
            ws = wb.create_sheet(title=sh["name"][:31])

        # Force all values as strings so Excel/Sheets do not auto-convert
        for c, h in enumerate(sh["headers"], 1):
            cell = ws.cell(row=1, column=c, value=str(h))
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center
            cell.border = thin_border

        for r_i, row in enumerate(sh["rows"], 2):
            for c_i, val in enumerate(row, 1):
                # Prefix ratio-like and numeric-looking text with nothing;
                # set number_format=@ (text) to block auto-conversion
                cell = ws.cell(row=r_i, column=c_i, value=str(val))
                cell.number_format = "@"
                cell.border = thin_border
                cell.alignment = center
                hdr = sh["headers"][c_i - 1] if c_i - 1 < len(sh["headers"]) else ""
                if "Trunc_e6" in hdr or hdr.endswith("_e6") or "e6" in hdr.lower():
                    cell.fill = e6_fill
                if "Trunc_e8" in hdr or "e8" in hdr.lower():
                    cell.fill = e8_fill
                if "Fraction" in hdr or hdr == "Exact_Ratio":
                    cell.fill = spoke_fill
                if "Notes" in hdr or "Nuance" in hdr or "Pole" in hdr:
                    cell.fill = pole_fill
                    cell.alignment = left
                if str(val) == UNDEFINED:
                    cell.fill = pole_fill

        if sh["name"] == "README_Instructions":
            ws.column_dimensions["A"].width = 120
            # Restyle title
            ws["A1"].font = Font(bold=True, size=16, color="1F4E79")
        elif sh["name"] == "Lookup_Dashboard":
            # dropdown on SELECT row, column B
            dv = DataValidation(
                type="list",
                formula1='"1/8,1/6,1/4,1/2,3/4,1"',
                allow_blank=False,
            )
            ws.add_data_validation(dv)
            # row 2 is SELECT_SPOKE_DEFAULT
            dv.add(ws["B2"])
            ws["B2"].fill = PatternFill("solid", fgColor="FFFF00")
            for col in range(1, 5):
                ws.column_dimensions[chr(64 + col)].width = 22
        else:
            for col in range(1, len(sh["headers"]) + 1):
                letter = chr(64 + col) if col <= 26 else "A"
                if col <= 26:
                    ws.column_dimensions[chr(64 + col)].width = 16

    out = out_dir / "Tims_Tables_SVCT_Edge_Lookup_v1.xlsx"
    wb.save(out)
    return out


def write_ods(sheets: List[Sheet], out_dir: Path) -> Path:
    try:
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table, TableRow, TableCell
        from odf.text import P
        from odf.office import Annotation
    except ImportError as e:
        raise RuntimeError(f"odfpy required for ods: {e}") from e

    doc = OpenDocumentSpreadsheet()

    def add_text_cell(tr: TableRow, text: str) -> None:
        # valuetype string — prevents numeric auto-conversion
        tc = TableCell(valuetype="string")
        tc.addElement(P(text=str(text)))
        tr.addElement(tc)

    for sh in sheets:
        table = Table(name=sh["name"][:31])
        # header
        hr = TableRow()
        for h in sh["headers"]:
            add_text_cell(hr, h)
        table.addElement(hr)
        for row in sh["rows"]:
            tr = TableRow()
            for val in row:
                add_text_cell(tr, str(val))
            table.addElement(tr)
        doc.spreadsheet.addElement(table)

    out = out_dir / "Tims_Tables_SVCT_Edge_Lookup_v1.ods"
    doc.save(str(out))
    # odfpy may write .ods or add extension; normalize
    if not out.exists():
        alt = Path(str(out) + ".ods")
        if alt.exists():
            alt.rename(out)
    return out


# ---------- CLI ----------

ALL_FORMATS = ("xlsx", "ods", "csv", "txt", "json", "jsonl")


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Tim's Tables multi-format builder (exact ratios, truncate never round)"
    )
    ap.add_argument(
        "--formats",
        default=",".join(ALL_FORMATS),
        help="Comma list: xlsx,ods,csv,txt,json,jsonl",
    )
    ap.add_argument(
        "--out",
        default=".",
        help="Output directory",
    )
    args = ap.parse_args(argv)

    wanted = [f.strip().lower() for f in args.formats.split(",") if f.strip()]
    unknown = [f for f in wanted if f not in ALL_FORMATS]
    if unknown:
        print(f"Unknown formats: {unknown}. Allowed: {ALL_FORMATS}", file=sys.stderr)
        return 2

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    sheets = build_all_sheets()
    violations = _assert_no_forbidden(sheets)
    if violations:
        print("FORBIDDEN CELL VALUES:", file=sys.stderr)
        for v in violations:
            print(" ", v, file=sys.stderr)
        return 3

    produced: Dict[str, List[str]] = {}
    errors: Dict[str, str] = {}

    if "csv" in wanted:
        paths = write_csv(sheets, out_dir)
        produced["csv"] = [str(p) for p in paths]
    if "txt" in wanted:
        paths = write_txt(sheets, out_dir)
        produced["txt"] = [str(p) for p in paths]
    if "json" in wanted:
        produced["json"] = [str(write_json(sheets, out_dir))]
    if "jsonl" in wanted:
        produced["jsonl"] = [str(write_jsonl(sheets, out_dir))]
    if "xlsx" in wanted:
        try:
            produced["xlsx"] = [str(write_xlsx(sheets, out_dir))]
        except RuntimeError as e:
            errors["xlsx"] = str(e)
    if "ods" in wanted:
        try:
            produced["ods"] = [str(write_ods(sheets, out_dir))]
        except RuntimeError as e:
            errors["ods"] = str(e)

    manifest = {
        "version": VERSION,
        "original_timestamp_anchor": ANCHOR_TS,
        "formats_requested": wanted,
        "produced": produced,
        "errors": errors,
        "sheets": [sh["name"] for sh in sheets],
    }
    man_path = out_dir / "MANIFEST.json"
    with man_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(json.dumps(manifest, indent=2))
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
