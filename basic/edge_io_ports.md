# edge_io_ports — pointer only (no sealed primitives)

Concept shell for USB / Edge Device / optional GPIO I/O flows.
Full as-drawn transcription, clarifications, mermaid, and UNDEF list:

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DEVICE_IO_FLOW_2026-10-05.md`

Sketch:

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DEVICE_IO_SKETCH_2026-10-05.jpg`

Not a GOSUB body. Not installed on device. GitHub push skipped unless parent stands next.

Port map (device class × port/capability table, UNDEF where not earned):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DEVICE_PORT_MAP_2026-10-05.md`

Locked answers A–F (2026-10-05 ET: iOS-first phone, ASUS TUF A15 Win 11, Hive ≥5 drones + optional Queen, adaptable for all, JBL Clip 4 + 2 camera-mics, code via BT/WiFi/USB):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_LOCKED_ANSWERS_2026-10-05.md`

Answers card: `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_UNKNOWNS_ANSWERS_A-F_2026-10-05.jpg`

Transport matrix (locked answer F: how code/records reach each device class over BT / WiFi / USB; SUGGESTED fallback USB → WiFi → BT, not locked; nothing paired):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_TRANSPORT_MATRIX_2026-10-05.md`

Manifest spec (draft sha256 refuse-to-run + provenance for BT/WiFi/USB; SUGGESTED fields; signing UNDEF; iOS delivery A/B/C as QUESTIONS; nothing implemented on devices):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_MANIFEST_SPEC_2026-10-05.md`

Pythonista phase 1 (iOS first; stdlib-only sha256 manifest check, refuse-to-run draft; BOX-only stub, not on any device; lead_filter.py optional import; I/O goals only):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_PYTHONISTA_PHASE1_2026-10-05.md`

Stub + demo: `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/targets/pythonista/phase1/manifest_check.py` (self-check 57/57; 60/60 with lead_filter). Not pushed.

Cellular note (F', 2026-10-05 ET: Cellular added to BT/WiFi/USB; "Q-tel" as-heard lead only, SKU UNDEF; Pi add-on modem OR smartphone tether; nothing purchased):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_CELLULAR_NOTE_2026-10-05.md`

Transport matrix now has a Cellular column (§2) and §3e; manifest spec `transport_used` allows Cellular|BT|WiFi|USB|UNDEF. Not pushed.

Data movement policy (G / DM-1…DM-7, 2026-10-05 ET: add/take files on demand or need; must work without the cloud; cloud + masked APIs only from time to time; home network; phone needs kept; box "but not only"):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_DATA_MOVEMENT_POLICY_2026-10-05.md`

Hardware as seen in Timothy's photos (labels only; Pi Zero 2 W, GY-521, BMM150, QMC5883P, USB stick; nothing wired or powered):

`/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/reference-map/EDGE_HW_INVENTORY_2026-10-05.md` (photos `EDGE_DESK_SETUP_2026-10-05.jpg`, `EDGE_HW_INVENTORY_2026-10-05.jpg`)

Pi Zero 2 W target stub (README only, sensors UNDEF-wired): `/workspace/session-scan-2026-10-05/generated-code/tims-edge-math/targets/pi_zero2_w/README.md`. Not pushed.

