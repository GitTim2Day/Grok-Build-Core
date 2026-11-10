# Tim's Tables — multi-format SVCT Edge Lookup

**Original timestamp anchor (America/New_York):** 2026-11-09 8:20 PM ET  
**Builder:** `work/create_tims_tables_multi.py`  
**Sealed original (untouched):** `original/create_tims_tables_xlsx.py` sha256 `67b5350844402b0b…`

## What the original builds

Six sheets in `Tims_Tables_SVCT_Edge_Lookup_v1.xlsx`:

1. **README_Instructions** — purpose, locked invariants, how to use  
2. **Core_Six_Ratios** — 6 spokes (1/8, 1/6, 1/4, 1/2, 3/4, 1) with degrees / radians / notes  
3. **Trig_e6** — sin / cos / tan at those spokes (e-6)  
4. **All_Matrix_e6** — matrix of Sin, Cos, Tan, 1/x, 2^x, 6^x, 8^x, log2, Frequency, Wavelength  
5. **Lookup_Dashboard** — bidirectional lookup (spoke dropdown in xlsx/ods)  
6. **Master_Flat_Data** — flat rows for PivotTables (Excel / Sheets / LibreOffice)

## What the multi builder adds

Same logical tables, written to:

| Format | Path | Needs |
|--------|------|-------|
| `.xlsx` | `out/Tims_Tables_SVCT_Edge_Lookup_v1.xlsx` | openpyxl |
| `.ods` | `out/Tims_Tables_SVCT_Edge_Lookup_v1.ods` | odfpy |
| `.csv` | `out/csv/<Sheet>.csv` (UTF-8) | stdlib only |
| `.txt` | `out/txt/<Sheet>.txt` (tab-separated) | stdlib only |
| `.json` | `out/Tims_Tables_SVCT_Edge_Lookup_v1.json` | stdlib only |
| `.jsonl` | `out/Tims_Tables_SVCT_Edge_Lookup_v1.jsonl` (four-pillar) | stdlib only |

### Exact-value rules (first-principles-tim / exact-ratio-loops / ratios-are-values)

- Ratios are the values; decimals are renderings only.  
- **Truncate never round** (√2/2 → e-6 is `0.707106`, not rounded `0.707107`).  
- **No stored zero** and **no ±∞** → cell text `UNDEFINED`.  
- Direction of signed trig lives in a Direction column; magnitudes stay positive.  
- Spreadsheet cells are written as **text** (`number_format=@` / ODS `valuetype=string`) so Sheets/Excel do not auto-convert ratios.

## CLI

```bash
python3 create_tims_tables_multi.py \
  --formats xlsx,ods,csv,txt,json,jsonl \
  --out /path/to/out
```

Omit heavy formats on a bare Pi:

```bash
python3 create_tims_tables_multi.py --formats csv,txt,json,jsonl --out ./out
```

## Usage per device

### A15 Windows / Linux (desktop)

- Full run with `--formats xlsx,ods,csv,txt,json,jsonl`.  
- Needs: Python 3.10+, `openpyxl`, `odfpy` (`pip install --user openpyxl odfpy`).  
- Open `.xlsx` in Excel or `.ods` in LibreOffice; PivotTables from `Master_Flat_Data`.

### Pi 5 ARM64 (edge)

- Prefer stdlib-only: `--formats csv,txt,json,jsonl`.  
- No pip required for those four.  
- Load `out/txt/*.txt` or `out/*.jsonl` into offline AI / const arrays.  
- If openpyxl/odfpy are already on the image, xlsx/ods work too — never install on the Pi without Timothy's validation.

### Google Sheets

1. Upload `out/csv/Core_Six_Ratios.csv` (and the other CSVs) via **File → Import → Upload**, or  
2. Upload the whole `.xlsx` to Drive and open with Sheets.  
3. All value columns are text — paste into arrays as strings; do not coerce to Number.

### LibreOffice / ODS

Open `out/Tims_Tables_SVCT_Edge_Lookup_v1.ods` directly. Values are string cells.

## Verification (2026-11-09)

- Data sheets **xlsx ↔ ods ↔ csv ↔ txt**: **0 cell diffs** (as strings).  
- Forbidden cells (`0`, `∞`, …): **0 hits**.  
- vs original xlsx: **intentional diffs** (216 on data sheets) — original used `round()`, stored `0.000000` and `∞`; multi uses truncate + `UNDEFINED` + ratio/Direction columns. Example: sin(45°) e-6 original `0.707107` (rounded) → multi `0.707106` (truncated). Original `8^(1/4)=2` was mathematically wrong; multi emits truncated `8^(1/4)`.

## Not done (awaits Timothy's OK)

- Drive / GitHub / email publish of this pack.  
- Saving into the project shelves (ledger → Notion → GitTim2Day → Drive → boot → memory).

## Pointers

- shelf · `/workspace/tims-tables-multiformat-2026-11-09/` · Tims Tables multi-format · see `SHA256SUMS` · 2026-11-09  
- original · Drive `1FYEIfKItl02cV32ObN1_wvoM7qIPocA2` · `create_tims_tables_xlsx.py` · SHA `67b5350844402b0b` · 2026-09-30  
