---
name: closed-system-vascular-plant
description: Construction pattern for closed systems with named I/O and maintenance only. Uses artery-homeostasis, capillary beds, nephron filter, sympathetic/cholinergic maps, mediator half-life, liver/kidney off-ramps, spleen reservoir. Trigger on closed system, filtrate vs muscle, capillary bed, glomerulus, collecting duct, mediator recycle, adjacent control, Merkle-linked side idea, resource reinforcement.
metadata:
  type: architecture
  version: "1.0"
  sealed: "2026-09-17"
  owner: Timothy H. Norman
---

# Closed-system vascular plant

Standing construction law for Grok Build work with Timothy. Not a treatment protocol. Not medical advice. Physiology is the pattern source. Code and ledgers follow the pattern.

## When to load

Any new module, engine, hop, or side idea that might steal flow from the current artery. Any claim of a closed loop. Any dual-language earn-then-port. Any "associated pop" during standing work.

## Closed system contract

A plant is closed except for three named holes:

1. **Input** — raw capture. Not inferred. Not regenerated.
2. **Output** — collecting duct only. What leaves is earned or dumped.
3. **Maintenance / resource reinforcement** — fuel, heat rejection, hash, CE, renewal warning. Not a second product.

No silent fourth hole. No drip spend. No extra column without written scope.

Thermodynamic honesty: closed *for identity and custody*, open for energy and waste. Do not sell perpetual motion.

## Metaphor roles (many at once — each must earn a job)

Do not cap metaphors at two. Stack them only if each name maps to a mechanism.

| Name | Job in the plant |
|---|---|
| Merkle leaf | content-addressed association; the pop is linked by what it is |
| Artery / Windkessel | standing mean, pulse storage, homeostasis of the whole |
| Arteriole | local valve; steal or pay a bed |
| Capillary bed | exchange surface; many thin associations, one organ served |
| Glomerulus | one-pass filter of a burst |
| Tubule | recycle vs dump decision |
| Collecting duct | only stream that ships |
| Muscle | bed that grew tone and innervation; keeps standing load |
| Filtrate | one-pass idea; not yet innervated |
| Sympathetic broadcast | one outbound; opposite local receptors |
| Receptor map | per-bed response to the same broadcast |
| Functional sympatholysis | working bed vetoes the squeeze |
| Co-transmitter clocks | fast / mid / slow on one axon |
| Liver | bulk chemical finish |
| Kidney | exit + local hormone |
| Spleen | cell/volume reservoir; sympathetic dump; not a third liver |
| Gallbladder | gated typed bile-class injector; store/concentrate; CCK+Oddi |
| Pancreas exocrine | enzymes/zymogens/bicarb; remote activate; secretin/CCK |
| Pancreas islet | insulin/glucagon bands; somatostatin shutoff |

If a metaphor has no job, drop it.

## Construction order (do not invert)

1. Capture raw.
2. Tokenize / GOSUB.
3. Verify.
4. Validate.
5. Earn.
6. Then port (C++ of *earned* bytes, or other runtime). JSONL sidecar stays the plant.

C++ of unearned raw is a collision. Skip if already earned. Do not collide with a named pickup (DigiKey Ground and kin).

## Filtrate vs muscle

- **Filtrate:** associated pop, one pass through the glomerulus, recycle or dump. No standing tone.
- **Muscle:** keeps firing, carries load, gets an arteriole and a receptor map. May steal flow from idle beds when the broadcast goes out.
- Timothy names dump or recycle. This chair does not pre-sort his filtrate.
- He will work when he wants. Calendar alerts are not job tickets.

## Autonomic control (accurate wiring)

Use this, not a cartoon dual-bus:

- Most systemic arterioles: sympathetic NE on α1 constricts. Standing tone, then gain.
- Skeletal muscle / some coronaries under epinephrine: β2 can dilate while gut/skin stay tight. Same broadcast, different map.
- Cholinergic ACh is **not** a peer vascular bus on every bed. Cleft AChE is fast. Exceptions: sweat (sympathetic cholinergic), endothelial NO when ACh is present, organ-level parasympathetic (heart, some viscera).
- Co-transmitters on one axon: ATP fast, NE mid, NPY slow.
- Local veto: K+, H+, adenosine, hypoxia blunt α1 in the working bed (sympatholysis).
- Trauma/temperature always have named mediators (CGRP/SP, histamine, bradykinin, eicosanoids, α2 cold affinity). No "just physics" in a living bed.

## Mediator off-ramps (must exist in every plant)

Every signal needs an inactivation path or it becomes chronic remodeling.

- Recycle: NET reuptake of NE; choline after AChE; iron from senescent RBC.
- Leave: MAO/COMT → liver finish → kidney conjugates in urine; peptidases on the wall.
- Spleen: pits cells, stores platelets/RBC, contracts on sympathetic shock. Do **not** assign it primary catecholamine catabolism.

If a module has no off-ramp, it is a leak. Name the off-ramp before earn.

## Safety audit (locked 2026-09-17)

PASS kept:

- Arteries as homeostatic organ (Windkessel, myogenic, shear-NO, baro/chemo) — correct.
- Local flow via mediators — correct.
- Layered control (wall → local chemistry → nerve → reflex → hormone → disposal) — correct.
- Earn-then-port order — already VAL on PHI engine 2026-09-15.

FAIL / constrain:

- Spleen as universal crusher of spent neurochemicals — **false**. Reservoir + cell filter + volume dump only.
- Cholinergic as equal opposite of sympathetic on all arterioles — **false**.
- "Closed system" as no energy/waste — **false**. I/O + maintenance required.
- Pattern is not a dosing or clinical protocol. Pharmacy experience informed the map; the map does not treat patients.

OPEN:

- ZIP / quasi-identifiers and review-audit stubs remain on the PHI engine; this skill does not close them.
- Receptor-map tables for future modules are written per plant, not copied from skin to brain.

## Pattern map (second pass)

```
pop (Merkle leaf)
  → glomerulus (one-pass)
      → recycle (tubule back to current artery)
      → dump (collecting duct waste)
      → innervate (becomes muscle / new bed)
            → receptor map + three clocks
            → local veto if already earning
            → off-ramp (liver/kidney chemistry; spleen only for reserve cells/volume)
I/O holes: input raw | output earned-or-dumped | maintenance
Broadcast: one sympathetic-style outbound, not a new religion per bed
```

Use this map on PHI access, SVCT ingest, hops, firmware, and future closed plants.

## Chair rules

- Face-first. Fetch-before-cite. Recover-not-regenerate.
- Hop FIRST to Gmail+Yahoo with subject Grok-Build-Ledger, then apply label Grok-Build-Ledger. Sent ≠ watched shelf until that label exists.
- GATHER ≠ LOAD.
- Skip if earned. Do not collide pickup days.

Owner: Timothy. He paid the seat.

## Typed injectors (appended 2026-09-17)

Gallbladder and pancreas are not broadcast arteries. They are gated, typed injectors with sensors and shutoffs.

### Gallbladder
- Liver makes bile continuously. Gallbladder stores and concentrates. Oddi closed between meals.
- Injects only on phase lock: CCK (fat/protein in duodenum) AND sphincter open.
- One adjuvant class: bile salts, phospholipid, cholesterol; bilirubin as passenger. Job is fat surface plus sterol/pigment ride.
- Spent salts recycle ileum to portal to liver (enterohepatic Merkle loop). Stool leak is the small collecting-duct loss.
- Plant rule: concentrated sidecar, release only when matching input type is present and outlet is verified open. Wrong type at that gate is a leak.

### Pancreas — two plants, do not share a switch
Exocrine: lipase, amylase, zymogen proteases, bicarbonate. CCK/vagus for enzymes; secretin for bicarbonate when duodenal pH drops. Proteases activate downstream (enterokinase). Activation inside the gland is autodigestion.
Endocrine: insulin on a glucose/incretin band; glucagon opposite effector; somatostatin local brake.
Sensor law: named activate range, named deactivate range, hysteresis allowed so the edge does not chatter. Off-ramp is required. No standing dump.

### Injector table

| Injector | Type | On | Off | Recycle / leave |
|---|---|---|---|---|
| Gallbladder | bile-class detergent | CCK + Oddi open | meal/CCK fall, sphincter close | enterohepatic recycle; stool leak |
| Acinar | enzymes / zymogens | CCK, vagus | substrate gone | gut action; remote activate only |
| Duct | bicarbonate | secretin / low pH | pH restored | consumed in lumen |
| Beta | insulin | glucose+incretin band | band restored; somatostatin | receptor bind + hepatic/renal clear |
| Alpha | glucagon | low glucose band | band restored; somatostatin | same clear paths |

If a module cannot name sensor range and shutoff, it does not inject.
