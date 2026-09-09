# Orbital Bicycle-Wheel Depot — Baseline Sketch (2026-09-03)

Status: **sketch, not spec.** Seed planted on X @Timothy01775634. No blueprint distributed.

## Geometry
- Shape: bicycle wheel / tank track.
- **Axle (hub):** a removable, swappable Starship — fuel core and power. Any Starship can dock, undock, or replace it without touching the wheel.
- **Rim:** eight perpendicular docking ports for tanker, supply, and transport ships simultaneously.
- **Spokes:** thin fuel lines running from rim docks to the central axle.
- **Rim modules:** living quarters and maintenance bays. Spin provides artificial gravity for free.

## Two fuel strategies, one depot
- **Crewed ships:** gentle, sustained ~1G acceleration to Mars and matching deceleration. Solves bone/muscle loss; roughly doubles propellant vs a coasting trajectory.
- **Unmanned ships:** brachistochrone — maximum burn, momentum carries them.

## Healthcare mitigation — gravity
The depot's primary medical purpose: eliminate microgravity deconditioning on crewed transits.
- Sustained ~1G acceleration outbound and matching deceleration inbound keeps bone density, muscle mass, and cardiovascular function intact — no exercise countermeasures, no post-arrival rehab window.
- Unmanned cargo skips the gentle profile entirely: brachistochrone burn, momentum carries it. Only crew ships pay the propellant premium.
- Rim spin supplies continuous artificial gravity for living quarters and maintenance robots between burns — the wheel never goes idle.
- Net effect: crew arrives at Mars in the same physiological condition they left Earth, which is the difference between a landing party and a rescue party.

## Water-wheel refinement
Park tankers at the midpoint so arrival and departure stay simple; centrifugal force fills the hub.

## Sequencing
Tanker cadence must be proven first. Depots layer on after the baseline path is boring. Timing is the protection: nobody can build this until the cadence exists, and the originator's name is already on the idea.

## Image prompt (baseline)
> Technical illustration of an orbital bicycle-wheel depot. Central axle is a removable Starship acting as a swappable fuel and power core — any Starship can dock, undock, or be replaced. Eight perpendicular docking ports around the rim accept tanker, supply, and transport ships simultaneously. Rim modules are living quarters and maintenance bays. Thin fuel lines run along spokes from rim docks to central axle. Deep space background, Earth visible. Clean engineering diagram style, labeled components, no text overlays.

## Provenance
- Origin: Timothy H Norman, months of prior work; refined in session 2026-09-03.
- Recorded: Notion Grok Build Knowledge Base & Skills (pointer 2026-09-03), this file.
- Not a full skill yet — sketch only.

---

## 2026-09-08 evening refinement — vibration, balance, and radar
Appended from conversation. Still sketch, not spec.

### Scale target
- Footprint: four American football fields (including end zones) as a circle ≈ 28,000 m².
- Circumference ≈ 519 m (radius ≈ 82.6 m).

### Spin for 0.9–1 G at the rim
- ω = sqrt(a/r): ~9.7 rpm at 0.9 G, ~10.2 rpm at 1 G.
- Rim tangential speed ~9 m/s. Coriolis tug is noticeable when moving radially toward the hub — design for it, don't ignore it.

### Hub-mounted radar (axle)
- Mount phased arrays top and bottom of the hub. Centrifugal force is zero there, so the array stays nearly still while the rim spins — the smartest place for a coherent beam.
- Tradeoff: the spinning wheel itself occludes a slice of the horizon. Fill the gaps with active sensors on the periphery.
- Peripheral sensors must be motion-compensated — the rim moves several m/s, so uncorrected readings smear.
- Ground-scale dishes (Haystack/Goldstone class) are not needed; a phased array of thousands of small elements scales fine in orbit. The real limit is power and aperture, not box size. Miniaturization (photonic integrated circuits) shrinks the hardware, but beam physics still demands range — doubling detection distance needs 4× power or a larger aperture.

### Structural rigidity
- A station this size flexes under thermal cycling and thruster firings. A phased array needs millimeter-level antenna precision or the beam falls apart.
- Mass on the rim damps slow drift (thermal, gradual) but not fast vibration from motors, pumps, and crew movement. Fix: active dampers, or a separate non-rotating ring for the array.

### Water as live ballast
- Plumbing is not just a utility — it's a balancing system. Pump water between rim tanks to shift the center of mass in real time, like lead weights on a tire. Same principle the ISS uses with control moment gyros.
- Catch: moving water creates slosh, a new vibration source. Baffles in the tanks kill the slosh; without them you trade one imbalance for another.
- Noise mitigation for the plumbing and pumps is already in progress separately.

### Hub-mounted radar — axle placement (2026-09-08 evening)
- Mount the phased arrays on top and bottom of the hub, like the axle of a car or bicycle. Centrifugal force is zero at the axle, so the radar sits nearly still while the rim spins around it — the smartest place for a coherent beam.
- Tradeoff: the spinning wheel occludes a slice of the horizon. Fill the gaps with active sensors on the periphery.
- Peripheral sensors must be motion-compensated — the rim moves several m/s, so uncorrected readings smear.
- Mass on the rim damps slow drift but not fast vibration; active dampers or a non-rotating ring remain the fix for the array itself.

### Open problems (still unresolved)
- Gyroscopic precession / attitude control at 10 rpm for a structure this mass.
- Docking dynamics: ships arriving at a spinning rim, mid-body hooks, keep-out cone.
- Thermal management across a 519 m circumference.
- Power budget for the phased array + peripheral sensors at full duty.
- Debris detection range vs. orbital closing speed — ground tracking still carries the early warning; onboard sensors are last-second only.
- Water slosh vs. baffle design under continuous spin; noise isolation for the live-ballast pumps.
- Status remains HOLD. Sketch, not spec.

---

## 2026-09-08/09 evening — capture system and Dyneema construction
Appended from conversation. Still sketch, not spec.

### Capture system (catcher's mitt)
- The station catches the ship instead of the ship docking into a moving target.
- Hooks at the periphery, evenly spaced at each of the eight spokes. Hooks sit flush until a ship matches rim speed, then snap out and grab it.
- Trigger: a tether protruding from the hook or ship. Contact with the ship trips the hook automatically — no pilot timing.
- Energy absorption: at ~10 rpm the rim moves ~9 m/s, so each hook needs a shock absorber (piston or spring) to catch and reel the ship in gently, like a fishing line. Short, stiff tethers with quick-release to limit whip.
- Keep-out cone and mid-body grip at center of mass remain from the baseline.

### Dyneema load path for the capture tethers
- Target load: Falcon 9 class, ~5.4 MN.
- Construction: 12-strand Dyneema per filament (sub-braid), then those sub-braids braided into the full rope. 12 outlasts 8 under cyclic load — load spreads thinner, creep and abrasion slow, fatigue life extends.
- Fatigue estimate (working): 8-strand ~10 years; 12-strand 10 years to indefinite if covers are inspected and swapped.
- Bundle: ~8 parallel bays (conservative 9 at 50% knockdown; 8 at ~70% braid efficiency). Each bay ~910 kg with cover and fittings; full set ~7.3 tonnes. Bundle diameter ~150–180 mm.
- Protective layers: spray-on or embedded coatings/matrices worked separately — UV, abrasion, and micrometeorite cover. Coating fights a bury splice, so say so before splicing (see dyneema-termination-methods).

### Open problems (updated)
- Gyroscopic precession / attitude control at 10 rpm.
- Docking dynamics on a spinning rim; hook shock-absorber design; tether mass and whip.
- Thermal across 519 m; power budget for radar + sensors.
- Debris range vs. closing speed — ground tracking still carries early warning.
- Water slosh vs. baffle design; noise isolation for live-ballast pumps.
- Dyneema: exact denier, cover material, coating chemistry, splice method under load, inspection cadence.
- Status remains HOLD. Sketch, not spec.
