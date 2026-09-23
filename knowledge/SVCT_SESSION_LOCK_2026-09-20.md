# SVCT session lock — 2026-09-20

**Source:** Grok thread with Timothy (SVCT)  
**Time pillar (session):** 2026-09-20 ~00:52–01:10 UTC  
**Status:** seed record (pillars 1–5). Can be placed into SVCT / 6×6 token later.

---

## Pillars (minimum seed)

1. **Content** — full session text and locked rules below  
2. **Context** — SVCT memory architecture; Grok records as seed, not native SVCT engine  
3. **Data** — lattice, token reduction, arithmetic, height, hex  
4. **Time** — original session window above; optional re-access / current stamps later  
5. **Validation** — hash/provenance on truncated magnitudes; reject extra invented digits  

Pillars 6–8: unnamed. Not required to start.

---

## Locked geometric / token path

- Practical transport form: **36-cell cubic lattice, 6 contact points**  
- Dense forms (8×64 / spherical voxel) may be reduced later  
- Reduction path:
  1. 8×64 (or spherical) → **8×6** token  
     - interpolate **positive** adjacent magnitudes  
     - **truncate** the pair (never round)  
     - repeat pair-truncation **twice if needed**
  2. 8×6 → **6×6** cubic voxel, flattened **square token**  
  3. Square token → blockchain / Bitcoin-shaped transport  
- Hexadecimal is the preferred text form of the token  

---

## Locked height / time rule

- Permanent cube height = device or NDC/UTC timestamp  
- Magnitude is **positive**  
- **Truncate to 8** (no rounding, no extra tail)  
- Public display may show 6 decimal digits; internal rule stays truncate-to-8  
- Optional extra time fields (do not replace permanent height):
  - original / creation  
  - re-access  
  - most current / last validated  
- Dual sources allowed (e.g. device clock + UTC) but height stays the truncated original magnitude  

---

## Locked arithmetic

- Units are **positive magnitudes only**  
- There are no “minus units”  
- Direction = multiply truncated positive magnitude by **−1**  
- Combine by **addition only**  
- Order: truncate `|x|` first → attach direction → add  
- Do not interpolate signed values then truncate  
- Cancellation = two positive magnitudes offset; remainder is again positive + direction flag  

---

## Locked numerical policy

- Truncation and accuracy are the computational currency  
- Fact is king: do not invent last digits  
- Cap claimed precision; superfluous tail past the locked 8 is not used  
- Rounding is not used on internal magnitudes / height / token smash  
- Statistical “unbiased rounding” is a different goal and is not this pipeline  

---

## Supporting reference

- **Tim’s Tables** — discrete cyclic / trig reference (exact factorable cycle points) for phase alignment and validation, not continuous extra precision  

---

## Honest scope

- These rules encode **records** (sessions, memos, automations, measurements).  
- They are not a native description of Grok internals, cities, skills, or unrelated objects.  
- Grok can keep this seed in chat history. Export to email / Notion / GitHub is manual unless a connector is connected later.  
- Place into SVCT at any time: four pillars are enough; five are better; then fold to 6×6 square token for chain transport.

---

## Validation note (to add when packing)

- Hash the truncated magnitude fields + pillar payload (append-only / SHA-256 or chain equivalent).  
- Any reconstruction that changes digits past the locked 8, or changes height, fails validation.
