# THERMAL_BAND_READINESS_2026-11-26

## Concept
Thermal-gated readiness signal for humanoid/edge units. Temperature at designated heat-rejection positions (feet pads, thigh backs) serves as a go/no-go band rather than a binary charged/not-charged flag.

## Architecture
- Floor threshold: below this, unit waits. Battery delivers poor current, ages faster.
- Ceiling threshold: above this, unit sheds heat (bladders, plates, convection).
- Band interior: cleared to operate. May be partially charged. Thermal readiness independent of state-of-charge.
- State-of-charge: tracked separately as its own range with its own threshold. Never conflated with thermal band.

## Heat Rejection Design
- Dyneema skin poor conductor (~0.4 W/m-K, 500x worse than aluminum). Abrasion layer, not heat path.
- Embedded thin aluminum or copper plates at feet pads and thigh backs do spreading.
- Bladders embedded near plates act as vessels: bring heat to surface for convection/radiation.
- Combined feet + thigh surface ~0.15 m^2. Natural air convection handles ~10-20 W steady.
- Peak bursts: temporary dump into phase-change pack or heat soak.
- No moving parts: passive conduction + convection + radiation.

## Monitoring
- Temperature sensors at each plate position.
- Signal fires when position hits appropriate temperature band.
- Escalation: self-fix first, recycle second, human last.
- Six-pillar SVCT provenance on every thermal event.

## Open Items
- Individualized thermal thresholds per unit type.
- Phase-change pack sizing for peak loads.
- Integration with motor cortex node.
- LabCorp-style monitoring dashboard for thermal history.

## Sibling Maps
- BLOOD_HOMEOSTASIS_2026-11-26
- SESSION_PATTERN_MAP_2026-11-26_MOTOR_CORTEX_SKELETON
- session-map-2026-11-25-tree-channel-model

Size 2253 bytes. SHA-256 fdcf709b5fe40d02414958e2be9e7245d6eaf3310e6460975d0130c6f3459344.