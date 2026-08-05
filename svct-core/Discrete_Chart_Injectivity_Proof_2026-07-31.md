# Discrete Chart + Canonicalizer — Injectivity Proof (exhaustive)

**Date:** 2026-07-31  
**File:** discrete_chart.py  
**Result:** INJECTIVE = True

## Chart decisions (now written down)

- No stored zero → centre-as-shell (k=1 is innermost shell, never a point)
- Pole-as-ring (geometry already present)
- Integer k (radial shell index); float only as display projection
- Hemisphere as ENUM (NORTH / SOUTH)
- Azimuth base-360 discrete (Nφ bins)
- Polar span 180 discrete (Nθ bins)
- Canonical form = unique representative of each physical location

## Proof method

Exhaustive enumeration on a finite chart (default K_max=4, N_theta=6, N_phi=12 → 576 intended physical points).

- Every intended point is a fixed point of `canonicalize`.
- Every intended point appears in the image.
- Out-of-range φ / θ / negative k are folded or rejected; no collisions among intended points.

This is a **decidable** proof, not a sampled probe (contrast with the vacuous T16).

## Why this layer, not the codec

Signed-r, φ-periodicity and θ-range defects are coordinate-system ambiguities. The codec correctly serializes whatever it is given. Bijection of physical location → token can only be proved after the coordinate system itself is injective. That proof now exists at the discrete chart layer.

## Explicit non-actions

- φ/θ channels were **not** closed inside ReferenceSVCT (would be harness-overfitting).
- Third blind wave on the codec suite is deferred until the coordinate layer is the target.

Version Clean. Finite. Musical. No Strings, No singularities, No infinity, No Zero's.
