TIMS_TABLES_PI_SEAL
====================
Rule: geometry in BASIC/C++/Python is algebra, not a library.
Pi is a sealed constant from Tim's Tables, not math.pi.

SEALED VALUES (truncation toward zero, e-8):
  PI_4   = 0.78539816
  PI     = 3.14159265
  PI_2   = 1.57079632
  TWO_PI = 6.28318530
  FOUR_PI= 12.56637061

DERIVED (table ratios, no trig call):
  4*pi / 64  = 0.19634984   (64-cell ring, per cell)
  4*pi / 360 = 0.03490658   (Tim's Table sector, per sector)
  4*pi / 6   = 2.09439510   (60-degree sector)

HOLOGRAPHIC CHECK:
  volume / surface = r/3
  residual recorded, never rewritten.

GATE INTEGRATION:
  GOSUB_SPHERE uses FOUR_PI from this seal.
  GOSUB_CLASSIFY unchanged: WAIT before seenFinite, REJECT after.
  Truncation: INT on absolute value, restore sign.

ERROR LOOP: finite, NaN, +inf, -inf, poison-NaN, None,
non-numeric, first-frame WAIT, 3.9->3, -3.9->-3,
box/triangle/trapezoid, seal chain, sphere residual,
Pass B two consecutive clean passes.

Sitting 2026-10-13T14:58:00-04:00. Size 974. SHA-256 998f321a663ca47687a07810f067d21784c3c07b7a10603b9ed99ddb96840fd8. Hash measured outside, no self-hash claim inside. Sibling of permanent-gel and hash-fruit maps. Not a merge. Ledger hop 1a1367ffdd20b426.