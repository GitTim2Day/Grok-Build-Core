# BrickFusion

**Family:** ONE-JOB  
**GOSUB ID:** BRICK_FUSE  
**Status:** PROMOTED  
**Direction:** forward (reverse = de-fuse, lossy)  
**Cost class:** Medium-High  
**Archived:** 2026-09-07

## Purpose
Multi-band sensor fusion with latency compensation. Merges asynchronous sensor streams into a single coherent frame without dropping the slowest band.

## Contract
- **Forward call:** BRICK_FUSE(bands[], timestamps[]) -> fused_frame, latency_map
- **Reverse call:** BRICK_FUSE.reverse(fused_frame) -> bands[] (approximate, lossy)
- **Shared state:** per-band latency budget, alignment window, drop policy
- **Direction tag:** forward-primary; reverse is reconstruction, not exact replay

## Method
Latency compensation aligns each band to a common time base before fusion. Bands arriving late are buffered within the alignment window; bands arriving too late are dropped per policy, never silently merged.

## Why it matters
Sensor fusion without latency compensation produces ghost artifacts — objects that appear in the fused frame but never existed in any single band. BrickFusion makes the fusion honest: every fused element traces to a real band at a real time.

## Held for owner
- Alignment window size per deployment
- Drop policy: drop-late vs. extrapolate-late
- Whether reverse reconstruction is needed or forward-only is sufficient

## Related
- KBLD-9 (cleans each band before fusion)
- KBL Pipeline (medical imaging, single-modality, no fusion needed)