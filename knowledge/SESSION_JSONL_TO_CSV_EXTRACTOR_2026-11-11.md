# SESSION JSONL TO CSV EXTRACTOR 2026-11-11

**File:** artifacts/session_jsonl_to_csv.py — 4964 bytes

**Contract:** Read session transcript as JSONL, one turn per line. Column headers plus row id form the key string. Each cell value lands in its comma-separated slot. Blank fields become NaN per locked rule. New columns append on the fly with NaN in every earlier row. Bidirectional index picks up new keys automatically on next load. Output drops straight into BiIndexSQLite or the plain CSV backbone without modification.

**Standing rules added 2026-11-11:**
- Rule 16: Audit gate non-optional before verbalization. Fresh stamp, delta check, top rules loaded, miss visible. No pass, no output.
- Rule 17: Dead-idea miss log. Five categories: false-claim, stale-clock, rule-skip, abandoned-idea, context-gap. Append-only, bidirectional, readable before new idea in same domain.
- Rule 18: Gmail at timnorman730@gmail.com is primary recovery shelf. Yahoo unreachable. Notion pointers only. If in Notion, body in Gmail. If in GitHub, body in Gmail.
- Rule 19: Five-category miss log with resurrection pass and component library. Salvaged fragments decomposed on death, indexed by function.
- Rule 20: Every response opens with live fetched stamp from clock tool. Never remembered value. One-minute freshness. Failure stated, not guessed.

**Combined boot set:** Priority first on every new sitting. Pointers only, bodies on shelves.

**HIT:** Extractor written, validated. **VAL:** Not yet run on live transcript. **Open:** Run on retained session export when CLI snapshot available.

**Stamp:** 2026-11-11T09:14-05:00 America/New_York
