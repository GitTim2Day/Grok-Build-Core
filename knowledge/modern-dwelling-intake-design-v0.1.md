# Modern Dwelling Intake Design — v0.1

**Status:** Draft skeleton. Iterate; promote to standalone skill once stable.
**Date:** 2026-09-03
**Source:** Derived from 2017 Dwelling Quote Form (dwelling-quote-form-2017-backup.md)
**Goal:** Conditional, photo-backed intake fixing 2017 weak spots (garbled half-bath, typed roof year, no roof condition, no flood zone).

## Design principles
- Conditional logic: "yes" to pool → open liability limits, dogs, breed, fence; "no" → hide.
- Same for roof age, claims history, rental use.
- Photo evidence over typed years: roof photo with date stamp is mandatory.
- Four grouped sections instead of a flat checklist.

## Section 1 — Property basics
- Address, county, year built, stories, construction type (brick/frame/stucco/other)
- Square footage (living, total), foundation (slab/crawl/basement — finished? SF)
- Garage/carport (# cars, attached/drive-under), fireplace (insert/masonry, gas logs yes/no)
- Baths: full count, half count (separate fields)

## Section 2 — Systems & updates
- Roof: install year (from photo), material, condition rating, last inspection date
- Plumbing, wiring, HVAC: year replaced + photo of equipment tags
- Central heat / central air: yes/no + age
- Water heater age, electrical panel age/amperage

## Section 3 — Hazards & protection
- Fire dept name + distance, nearest hydrant (within 1000 ft?)
- Smoke detectors (#), fire extinguishers (#), deadbolts, monitored alarm (central/local/none)
- Pool (yes/no → liability questions), trampoline, dogs (breed/count), fence
- Flood zone (FEMA map lookup), wildfire risk, distance to coast if applicable
- Claims in past 6 years (date, type, amount), non-renewal/cancellation history

## Section 4 — Scheduled valuables & limits
- Guns ($ limit), jewelry ($), silver/collectibles ($), electronics, musical instruments
- Mortgagee, closing attorney contact

## Gaps the 2017 form missed
- Roof condition photo + material (not just year)
- Flood zone
- Electrical panel details
- Dog breed (liability)
- Roof age-based surcharge flag

## Next steps
- [ ] Review field list with agent or carrier requirements
- [ ] Build conditional prototype (Notion form or Gamma)
- [ ] Add photo-upload requirement spec
- [ ] Compare against current State Farm / carrier intake for parity
