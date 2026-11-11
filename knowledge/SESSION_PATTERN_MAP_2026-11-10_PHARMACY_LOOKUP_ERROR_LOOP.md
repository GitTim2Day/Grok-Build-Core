# SESSION_PATTERN_MAP_2026-11-10_PHARMACY_LOOKUP_ERROR_LOOP

America/New_York: 2026-11-10 19:56 EST

## Pattern Match and Map

Error-test / mitigate loop on pharmacy_ingredients_lookup.py.

Start SHA: 0f2ac8bb25d6053e711ec83520c0ae9dd1b59225d67a13332e79ba738176c0b7
Mitigated SHA: 15f0b2c949d9e5e21b7eb607049f53975753d7ce5319bd524b574857677f0253

Defect found: --append with insufficient arguments fell through to lookup and returned NOT FOUND.
Mitigation: --append now requires name + H|NH + food_gras + primary_use; otherwise prints usage and returns 1.
Additional guards: empty name rejected; hazardous must be H or NH; already_present still returns 0.

## Audit (error suite)

22 cases: 0 failures.
- validate PASS (27 rows, 8 anchors)
- case and whitespace normalize
- empty / missing name → NOT FOUND
- bad --append arity → usage, exit 1
- empty name / bad hazardous → rejected
- already_present returns 0
- append does not mutate sealed TABLE (lookup of candidate still NOT FOUND; validate still PASS)
- long name, unicode, quotes, path-looking key all stay in the candidate log only
- JSON escaping holds

## Pattern Match Again

Loop closed. Sealed table protected. Append path append-only and argument-safe. Nearly flawless on the tested surface.

Open: none on the lookup. Gate wiring still only if later named.
