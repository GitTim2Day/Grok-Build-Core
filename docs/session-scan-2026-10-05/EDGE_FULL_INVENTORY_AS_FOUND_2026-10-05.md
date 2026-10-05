# EDGE FULL INVENTORY — AS FOUND (Timothy Norman)
Written: 2026-10-05 ~7:05 PM ET · **ADXL355 DigiKey lock:** 2026-10-05 ~7:05 PM ET · Build merge: 2026-10-05 ~7:00 PM ET
Boot this pass: `bwbasic /workspace/hybrid-boot/BOOT.bas </dev/null` → PRINT `0.70710678`, exit 0.
Fail-closed. **As-found only** — every row cites a Gmail message id, photo path, or DigiKey label read. Nothing invented beyond what the label/photos/voice state. Prior `i2cdetect` **1d** for ADXL355 is cited from research_boot_catchup only (not re-run). No GitHub push. Nothing published. Share Catalog stays sealed.
Build merge source: `/workspace/inventory-report-2026-10-05-build.md` (S10). DigiKey photos: `EDGE_DIGIKEY_ADXL355_LABEL_2026-10-05.jpg` · `EDGE_ADXL355Z_BOX_2026-10-05.jpg`.

Status legend (strongest evidence wins; lower tiers are kept in the provenance column):
| Status | Meaning |
|---|---|
| **SEEN** | Visible in Timothy's 2026-10-05 photos (label/shape). Not powered, wired, or tested. |
| **STATED** | Timothy said or wrote he has it (voice / handwritten card / email signature). Not verified on a device. |
| **NAMED-IN-HAND** | Earlier Grok holdings call it in hand / in use. Not photo-confirmed today. |
| **ACTIVE-POC** | On the 2026-09-21 ACTIVE afferent inventory table. |
| **LIST-2025** | On the April–May 2025 parts/cost list. **Planning list only** — no purchase, order line, or actual cost found (cost sheet "Actual Cost" column: 0 of 24 filled). |
| **UPGRADE / OLD-REC** | Named as upgrade path or old recommendation list; not current floor. |
| **SUMMARY-ONLY** | Named in a Gmail/subject/summary line; source file or body **ABSENT** on box. Not ownership. |
| **DEFERRED** | Source explicitly deferred the add-on. Not ownership. |
| **CITED-POSSIBLY** | Timothy or a share used "possibly" / mixed wording. Not owned evidence. |
| **PROCESS-NAME** | Receipt / process id only; **0 order lines**. |
| **UNDEF** | Not earned. |

---

## A) Source register (by date, ET)

| # | Date (ET) | Source | Provenance | sha256 (box copy) |
|---|---|---|---|---|
| S1 | 2025-04-14 1:49 PM | Gmail "Item,Category,Purpose,Preferred Sourcing,Cost Range" — attachment `expandable.csv` | msg/thread `196356c20d7ba729` (from [email masked] → [email masked]; body "Sent from Tim Norman's iPhone") · box `inventory-gmail-2025/expandable.csv` | `ef7d3ef2…6c10f13` |
| S2 | 2025-04-14 3:54 PM | Gmail "Inventory progress" — attachment `expandable_cleaned copy.xlsx` (sheet "in", 25×5; xlsx created 2025-04-14, author Tim Norman) | msg/thread `19635ddd359d3297` · box `inventory-gmail-2025/inventory_progress.xlsx` | `02fc8c2e…3f251fe` |
| S3 | 2025-04-15 7:42 PM | Gmail "More Parts 4/15/2025" — attachment `Document (8).docx` (author Tim Norman) | msg/thread `1963bd561599f801` · box `inventory-gmail-2025/more_parts.docx` | `ed4bda5d…3ea13` |
| S4 | 2025-04-15 9:07 PM | Gmail "First Order Raspberry Pi kit +" — attachment `Document (8) copy.docx` (author Tim Norman) | msg/thread `1963c22dcefe3b84` · box `inventory-gmail-2025/first_order_pi_kit.docx` | `f021d855…29498` |
| S5 | 2025-05-01 8:56 AM | Gmail "Cost sheet" — attachment `expandable_cleaned copy.xlsx` (sheet "in", 25×6: S2 + empty "Actual Cost" column) | msg/thread `1968beb3a98c8ee4` · box `inventory-gmail-2025/cost_sheet.xlsx` | `4d4fa077…2ce052` |
| S6 | 2026-09-21 1:02 PM | ACTIVE INVENTORY — IMU POC | `/workspace/_bill_yesterday/ACTIVE_INVENTORY_IMU_POC_2026-09-21.md`; mirrored by Gmail "Grok-Build-Ledger 2026-09-21 IMU POC MAG-QMC + IMU-GY521 afferent/efferent" msg `1a0c4edd69769458` (1:05 PM ET; snippet only read) | — |
| S7 | 2026-10-05 ~6:35–6:50 PM | Locked answers A–F + F' (card + voice) | `reference-map/EDGE_LOCKED_ANSWERS_2026-10-05.md` | — |
| S8 | 2026-10-05 ~6:46 PM | Photos (desk + parts) as-seen read | `reference-map/EDGE_HW_INVENTORY_2026-10-05.md` (+ `.jpg` `33d7faad…ef0`, desk `.jpg` `7878da09…c8`) | — |
| S9 | 2026-10-05 ~6:51 PM | Local Grok holdings hunt (concurrent) | `reference-map/EDGE_INVENTORY_FROM_GROK_HOLDINGS_2026-10-05.md` (Pi Zero date corrected 2025-10-03 this merge) | — |
| S11 | 2025-04-18 10:48 PM | Gmail **Hardware_List.txt** body (no attachments) | msg `1964bf2e31c79d4a` · box `inventory-gmail-2025/Hardware_List_body_1964bf2e31c79d4a.txt` | `30022034…af6d179c` |
| S12 | 2026-10-05 voice | Better **accelerometer** (Timothy correction: said altimeter by mistake) — DigiKey ~$90 after packaging/shipping (few bucks back); unsoldered for pro solder | chat | — |
| S10 | 2026-10-05 ~6:50–7:05 PM | Build agent inventory report (fail-closed) | `/workspace/inventory-report-2026-10-05-build.md` sha256 `7d3cdcdc…aafcf` | — |
| S13 | 2026-10-05 ~7:03–7:05 PM | DigiKey **ADXL355** photos (label + Analog Devices box/bag) — locks S12 SKU | `reference-map/EDGE_DIGIKEY_ADXL355_LABEL_2026-10-05.jpg` sha256 `017725d9…fe83d4659` · `EDGE_ADXL355Z_BOX_2026-10-05.jpg` sha256 `5ddbeecb…db849fefce83d54` | see label fields below |

Gmail ids above were re-read this pass (read-only, attachment filenames + dates confirmed). All five 2025 messages are Timothy emailing himself from his iPhone; bodies carry no text beyond the signature (S1 body repeats the CSV header).

**Content check on the 2025 files (parsed with openpyxl / python-docx, box only):**
- S1, S2, S5 hold the **same 24 rows in the same order** (10 Software + 14 Hardware). S2/S5 store "Free" cells as `0`; S5 adds an "Actual Cost" column that is **empty on all 24 rows**.
- S3 and S4 are the **same hardware subset** (12 lines: battery, BMS, 6 sensors, camera, OLED, VR goggles, Quectel EC25), S4 just re-line-broken. Both carry the note: "though the Raspberry Pi 5 has built-in WiFi/Bluetooth, this module may enhance cellular connectivity if needed [web:4]".
- S4's subject says "First Order Raspberry Pi kit +", but the attachment lists **no kit SKU, quantities, vendor order, or prices paid** → what was actually ordered = **UNDEF**.

---

## B) Section by source date

### B1) 2025-04-14 → 2025-05-01 — Gmail parts / cost list (S1–S5)

Software (10) — all **LIST-2025**, none claimed installed:
| # | Item | Purpose (as written) | Sourcing (as written) | Cost range |
|---|---|---|---|---|
| SW1 | Bitdefender | Antivirus for dev environment | bitdefender.com | $60/year |
| SW2 | Wireshark | Network monitoring | wireshark.org | Free |
| SW3 | ClamAV | Antivirus for Raspberry Pi 5 | `sudo apt install clamav` on RPi OS | Free |
| SW4 | UFW | Firewall for RPi 5 security | `sudo apt install ufw` on RPi OS | Free |
| SW5 | Docker | Sandboxing for dev/testing | `sudo apt install docker.io` on RPi OS | Free |
| SW6 | Bandit | Static code analysis | `pip install bandit` | Free |
| SW7 | Safety | Dependency vulnerability check | `pip install safety` | Free |
| SW8 | Python 3 | Core language for screener | python.org | Free |
| SW9 | Flask | API for smartphone interfacing | `pip install flask` | Free |
| SW10 | ROS 2 Humble | Robotic control on RPi 5 | docs.ros.org/en/humble | Free |

Hardware (14) — as written; "screener" = the 2025 project's own word:
| # | Item | Category (as written) | Purpose | Sourcing | Cost range | In S3/S4? |
|---|---|---|---|---|---|---|
| HW1 | Raspberry Pi 5 | Hardware | Base unit for screener | raspberrypi.com | $80–$100 | named in note only |
| HW2 | MicroSD Card (64GB) | Hardware | Storage for RPi OS and data | Amazon (e.g., SanDisk 64GB) | $10 | no |
| HW3 | Lithium-Ion Battery (3.7V, 2000mAh) | Hardware | Power source for RPi 5 | DigiKey or Adafruit | $10–$20 | yes |
| HW4 | Battery Management System (BMS) | Hardware | Monitors Li-ion battery safety | Adafruit or SparkFun | $15–$30 | yes |
| HW5 | Temperature Sensor (DHT11) | Hardware | Monitors temp for reliability | Amazon or Adafruit | $5 | yes |
| HW6 | Ultrasonic Sensor (HC-SR04) | Hardware (Sensor) | Obstacle detection | Amazon or Adafruit | $5 | yes |
| HW7 | IMU (MPU-6050) | Hardware (Sensor) | Terrain analysis (inclines) | Amazon or Adafruit | $5 | yes |
| HW8 | Current Sensor (ACS712) | Hardware (Sensor) | Monitors battery current | Amazon or DigiKey | $5–$10 | yes |
| HW9 | Voltage Sensor (25V max) | Hardware (Sensor) | Monitors battery voltage | Amazon or DigiKey | $5–$10 | yes |
| HW10 | LIDAR Sensor | Hardware (Sensor) | Advanced obstacle detection | Amazon or DigiKey (e.g., VL53L0X) | $20–$50 | yes |
| HW11 | High-Resolution Camera | Hardware (Expansion) | Object recognition | Raspberry Pi Camera Module | $25–$40 | yes |
| HW12 | Bluetooth Display Screen (1.5-inch OLED) | Hardware (Expansion) | Visual feedback | Adafruit or SparkFun | $15–$25 | yes |
| HW13 | VR Goggles | Hardware (Expansion) | Immersive navigation previews | Amazon (Google Cardboard) | $10–$30 | yes |
| HW14 | WiFi/Cellular/Bluetooth Module (**Quectel EC25**) | Hardware | Connectivity for RPi 5 | DigiKey or Mouser | $30–$50 | yes |

Notes: "e.g., VL53L0X" and "e.g., SanDisk" are examples in the list, not chosen models. Cost ranges are planning estimates, not prices paid. List total range not computed (mixed "$60/year", "Free", ranges — would be invented precision).

### B2) 2026-09-21 — ACTIVE INVENTORY IMU POC (S6)
| ID | Board | Job | Bus (ASSERTED typical, not scanned) | Standing |
|---|---|---|---|---|
| MAG-QMC | QMC5883P | heading | I2C ~0x2C | ACTIVE afferent |
| IMU-GY521 | GY-521 (MPU-6050 class) | accel + gyro | I2C 0x68 / 0x69 | ACTIVE afferent, POC floor |
| — | ADXL355 (EVAL-ADXL355Z) | upgrade path → **OWNED SEEN 2026-10-05** | I2C prior cite 1d | DigiKey SO 101583476 / PN 505-EVAL-ADXL355Z-ND; still not POC floor until bind ticket VAL's |
| — | HMC5883L | old rec list | — | **not this board; never load HMC driver on QMC** |
| — | Shepherd **Pi 5** | host for Grok CLI pin 1.0.25 | — | not flashed this sitting |
Open: `i2cdetect -y 1` never earned.

### B3) 2026-10-05 — Locked answers A–F/F' (S7)
JBL Clip 4 (1×) · cameras with built-in mic (2×, models/connection UNDEF) · ASUS TUF Gaming A15, 64 GB RAM, Windows 11 (or 10 & 11) · phone: "Both but start with iOS" · Hive = ≥5 drones + optional Queen (or Maiden) — **definition, not owned hardware** · transports BT / WiFi / USB / Cellular ("Q-tel" as heard).

### B4) 2026-10-05 — Photos (S8; as-seen labels)
Pi Zero 2 W (Adafruit sticker P5291 / P5291A, `adafru.it/5291`, date **2025-10-03** — re-cropped earlier; **Build S10 zoom-confirmed**; S9 holdings line corrected this merge from misread 2023) · HiLetgo GY-521 MPU-… module (X000ZP9S7H) · BMM150 3-axis magnetometer (X003YC93NR, brand UNDEF) · Adafruit QMC5883P Magnet QT (P6388, W36629-A) · Micro Center USB3.1 128 GB flash drive · white Lightning cable (other end UNDEF) · jumper wires · Dell monitor · webcam on monitor (model UNDEF) · ASUS TUF GAMING A15 · keyboard · pointing device · small black vented case with green light (UNDEF) · small board on jumper bundle (UNDEF) · earbud case engraved with a name (personal item — not project inventory).

### B5) 2026-10-05 — Local Grok holdings (S9) — adds only
Pi 5 "in hand" (Notion cite `at-integration-hold-2026-09-09` via HUNT 2026-09-20) · SHILLEHTEK accelerometer (Notion cite only; SKU UNDEF) · USB webcam + speakers / printer WiFi+BT (named aims) · target classes RP2040, STM32, Rabbit R1 (**catalog targets, not owned**). Jetson moved to §B6 / C6 as CITED-POSSIBLY.

### B6) 2026-10-05 — Build inventory merge (S10) — adds / updates only
Fail-closed from `/workspace/inventory-report-2026-10-05-build.md`. No ownership invented.

| Item | Status as earned | Provenance |
|---|---|---|
| **Camera Module 3** (+ USB mic/speaker etc.) | LIST-2025 / PLANNING | Gmail **2025-04-18** body `1964bf2e31c79d4a` now on box (S11). Full HL1–HL13 in §B7. Relation to LIST-2025 HW11 / C2#26 = **UNDEF** |
| **NEO-6M GPS** (Pi 5 add-on) | DEFERRED | Gmail **2025-05-07** — "GPS deferred as add-on" (same research_deep_history L29) |
| **T-Cobbler / PiGPIO** | SUMMARY-ONLY | Gmail **2025-04-21** id `196592c54cef81ac` (cite in ARCHITECTURE_svct…Drive.md / Build report) — body not opened this merge |
| **LocalSend** | SOFTWARE NAMED | Grok share createTime **2026-08-10** (starred): iPhone ↔ ASUS TUF A15; phone name "Fresh Banana". Install state **UNDEF** |
| **ADXL355** (EVAL board) | **SEEN owned** (S13) + CODE evidence | DigiKey label PN **505-EVAL-ADXL355Z-ND** / MFR **EVAL-ADXL355Z**; SO **101583476** (= SVCT-DK-101583476); INV **[INV masked]**; date **13-SEP-2026 15:23**; bag **ADXL355Z S/N [S/N masked]**. Driver: ETMR **48/48**; prior `i2cdetect` **1d**. Unsolded for pro solder (S12). |
| **Jetson Nano / Orin Nano** | CITED-POSSIBLY | Voice 2026-09-21 "possibly … Jetson Nano Orin, that $249 version"; share 2026-07-08 "Pi 5 + Jetson Nano". Not photo-confirmed |
| **SVCT-DK-101583476** | **ORDER LINE EARNED (this part)** | SO# on DigiKey label = **101583476** (S13) matches SVCT-DK-101583476. Line: PN 505-EVAL-ADXL355Z-ND qty 1. Other DigiKey lines still UNDEF. |
| Quectel EC25 | (already listed) | S1–S5 HW14 / C2#29 — no change |
| Pi Zero 2 W bag date | CONFIRMED **2025-10-03** | Build zoom of photo label |
| ASUS A15 extras (notes only) | NAMED in shares/voice | "2024 RTX 3050" (Ghostty share); "two terabytes" (voice) — not re-verified on unit this pass |

---

### B7) 2025-04-18 — Gmail Hardware_List.txt body (S11) — **PLANNING only**
Message id `1964bf2e31c79d4a` · Fri 2025-04-18 10:48 PM ET · body only (attachments: none) · box copy `inventory-gmail-2025/Hardware_List_body_1964bf2e31c79d4a.txt` sha256 `30022034eab98de4f1fba9fe507ad36301230bfab24d4fdbbc0f79feaf6d179c`.
**Status for every row below: LIST-2025 / PLANNING — ownership UNDEF** unless separately earned (Pi 5 NAMED-IN-HAND; Camera Module 3 remains SUMMARY→now BODY-CITED planning).

**Hardware_List.txt** (as written):
| # | Item |
|---|---|
| HL1 | Raspberry Pi 5 |
| HL2 | HiLetgo 5-piece Voltage Detection Module |
| HL3 | SHILLEHTEK 2-piece Pre-Soldered Accelerometer |
| HL4 | 128GB+ microSD |
| HL5 | Raspberry Pi Camera Module 3 |
| HL6 | USB microphone |
| HL7 | USB speaker |
| HL8 | 2.8" TFT display |
| HL9 | 1TB SSD |
| HL10 | HDMI monitor |
| HL11 | DHT22 temperature/humidity sensor |
| HL12 | Air quality sensor |
| HL13 | Cluster of Raspberry Pi 5s |

**Software_List.txt** (planning names only): TensorFlow Lite · PyTorch · Elasticsearch 8.x · Kibana · OpenCV · SpeechRecognition · eSpeak · Pygame · Grafana · Cassandra · VS Code · Flake8 · Raspberry Pi OS · Suricata · Python 3.3.

**Concepts_List.txt** (concepts, not hardware): Neural Net (3-D/4-D) · Appendable Data Streams · Reliability Scoring · Probability Expression · B-tree Indexing · Hybrid Indexing (B-tree + columnar) · Choice Algorithm · Elasticsearch Hashtag Search · Multi-Sensory Input (motion, vision, voice) · Environmental Awareness (self-awareness) · Dashboard-Driven Node Actions · Master Dashboard · Accessibility (speaker/display for blind/deaf) · HIPAA Compliance · Bot Screening · O(log n) Decision Trees · JSON/Bundles · Internet Input · Rapid Recall · Contextual Awareness · Total Integration Solution · Machine Awareness · Row-to-Row Indexing.

### B8) 2026-10-05 — DigiKey ADXL355 locked (S12 voice + S13 photos)
Timothy voice (S12): meant **accelerometer** (not altimeter); DigiKey ~**$90** after packaging/shipping (few bucks back); **unsoldered** for professional solder.

Timothy photos (S13) lock the SKU / order line:
| Field | Value (as read from label/bag) |
|---|---|
| DigiKey PN | **505-EVAL-ADXL355Z-ND** |
| MFR PN | **EVAL-ADXL355Z** |
| Description | EVAL BOARD FOR ADXL355 |
| Manufacturer | Analog Devices Inc |
| Qty | **1** |
| INV# | **[INV masked]** |
| SO# | **101583476** (= prior process name **SVCT-DK-101583476**) |
| Label date | **13-SEP-2026 15:23** |
| Bag mark | **ADXL355Z** · S/N **[S/N masked]** |
| Photos | `EDGE_DIGIKEY_ADXL355_LABEL_2026-10-05.jpg` · `EDGE_ADXL355Z_BOX_2026-10-05.jpg` |

Status: **SEEN owned · DigiKey order line earned for this part · pending professional solder**. Merges former C3#30 (upgrade/code-only) + former C1b#46 (STATED better accelerometer). Relation to SHILLEHTEK planning (C2b#37) still **UNDEF**. Not wired/tested this sitting. Not GY-521/MPU-6050 (C1#5).


## C) MERGED as-found inventory (deduped)

### C1) Hardware — owned evidence (SEEN / STATED / NAMED-IN-HAND / ACTIVE-POC)
| # | Item | Status | Provenance | Open (UNDEF) |
|---|---|---|---|---|
| 1 | ASUS TUF Gaming A15 laptop, 64 GB RAM, Win 11 (or 10 & 11) | SEEN + STATED | S7 L-B; S8 desk photo; S10 voice "two terabytes"; Ghostty share names "2024 RTX 3050" | model year/SKU; GPU / storage on *this* unit not re-verified this pass |
| 2 | iPhone (iOS phone) | STATED | S7 L-A "start with iOS"; S1–S5 bodies "Sent from Tim Norman's iPhone" (2025) | model, iOS version, Pythonista version |
| 3 | Raspberry Pi 5 ("shepherd") | NAMED-IN-HAND + LIST-2025 | S6 (CLI pin 1.0.25); S9 Notion "Pi 5 in hand"; S1–S5 HW1 | not in today's photos; pin map; OS |
| 4 | Raspberry Pi Zero 2 W (Adafruit 5291) | SEEN | S8 | header soldered?, microSD/OS, PSU |
| 5 | GY-521 IMU (MPU-6050 class), HiLetgo | SEEN + ACTIVE-POC + LIST-2025 | S8; S6 IMU-GY521; S1–S5 HW7 "IMU (MPU-6050)" | chip suffix cut off on label; I2C addr not scanned |
| 6 | Adafruit QMC5883P Magnet QT (6388) | SEEN + ACTIVE-POC | S8; S6 MAG-QMC | I2C addr not scanned |
| 7 | BMM150 3-axis magnetometer | SEEN | S8 (not on S6 POC table — do not merge into POC without a new lock) | brand; purpose |
| 8 | Micro Center USB3.1 128 GB flash drive | SEEN | S8 | contents (not read) |
| 9 | Lightning cable (white) | SEEN | S8 | other end |
| 10 | Jumper wires (assorted) | SEEN | S8 | — |
| 11 | Dell monitor | SEEN | S8 desk | model/ports |
| 12 | Webcam on monitor | SEEN | S8 desk | model; whether one of the 2 cam/mics |
| 13 | Keyboard (full size, no cable seen) | SEEN | S8 desk | model; wireless? |
| 14 | Pointing device | SEEN | S8 desk | type |
| 15 | Small black vented case, green light on | SEEN | S8 desk | **what it is** (ask Timothy) |
| 16 | JBL Clip 4 Bluetooth speaker (1×) | STATED | S7 E addendum | pairing |
| 17 | Cameras with built-in microphone (2×) | STATED | S7 E addendum | models; USB vs CSI |
| 47 | **ADXL355** eval board (Analog Devices **EVAL-ADXL355Z**) | **SEEN** + STATED cost + CODE | S13 DigiKey label/box; S12 voice ~$90 after pkg/ship; S6/S10 driver ETMR 48/48, prior i2cdetect **1d** | soldered?; host board; bus scan this sitting; bind ticket VAL's (still not POC floor) |

### C2) Hardware — 2025 planning list only (LIST-2025; no purchase evidence)
| # | Item | Provenance | Note |
|---|---|---|---|
| 18 | MicroSD card 64 GB | S1/S2/S5 HW2 | |
| 19 | Li-ion battery 3.7 V 2000 mAh | S1–S5 HW3 | |
| 20 | Battery Management System (BMS) | S1–S5 HW4 | |
| 21 | DHT11 temperature sensor | S1–S5 HW5 | |
| 22 | HC-SR04 ultrasonic sensor | S1–S5 HW6 | |
| 23 | ACS712 current sensor | S1–S5 HW8 | |
| 24 | Voltage sensor (25 V max) | S1–S5 HW9 | |
| 25 | LIDAR sensor (e.g., VL53L0X) | S1–S5 HW10 | model is an example only |
| 26 | High-resolution camera (Raspberry Pi Camera Module) | S1–S5 HW11 | may or may not be one of the 2 cam/mics — UNDEF |
| 27 | Bluetooth display 1.5-inch OLED | S1–S5 HW12 | |
| 28 | VR goggles (Google Cardboard) | S1–S5 HW13 | |
| 29 | **Quectel EC25** WiFi/Cellular/Bluetooth module | S1–S5 HW14 | **Timothy's own 2025 list spells the "Q-tel" lead: Quectel EC25.** Owned/ordered: UNDEF. Not seen in photos. |


### C2b) Hardware — 2025-04-18 Hardware_List.txt planning (S11 body; ownership UNDEF)
| # | Item | Provenance | Note |
|---|---|---|---|
| 36 | HiLetgo 5-piece Voltage Detection Module | S11 HL2 | distinct from S1–S5 HW9 "Voltage Sensor (25V max)" naming — do not merge without lock |
| 37 | SHILLEHTEK 2-piece Pre-Soldered Accelerometer | S11 HL3 | elevates prior Notion-only name to email body; vs ADXL355 = **UNDEF** |
| 38 | USB microphone | S11 HL6 | planning; may relate to STATED 2× cam/mic — UNDEF |
| 39 | USB speaker | S11 HL7 | planning; JBL Clip 4 is separate STATED unit |
| 40 | 2.8" TFT display | S11 HL8 | planning |
| 41 | 1TB SSD | S11 HL9 | planning |
| 42 | DHT22 temperature/humidity sensor | S11 HL11 | distinct from LIST-2025 DHT11 (HW5/C2#21) — do not merge |
| 43 | Air quality sensor | S11 HL12 | model UNDEF |
| 44 | Cluster of Raspberry Pi 5s | S11 HL13 | planning cluster; single Pi 5 remains NAMED-IN-HAND |
| 45 | 128GB+ microSD (Hardware_List) | S11 HL4 | overlaps C2#18 64GB planning — keep both rows; sizes differ |

HL1 Pi 5, HL5 Camera Module 3, HL10 HDMI monitor already covered elsewhere (C1#3, C6#32, C1#11 Dell monitor — relation UNDEF).

### C1b) Hardware — STATED owned pending install
| # | Item | Status | Provenance | Open (UNDEF) |
|---|---|---|---|---|
| — | *(former #46 Better accelerometer)* | **MERGED into C1#47 ADXL355** | S12+S13 2026-10-05 | pending professional solder remains open on C1#47 |

### C3) Hardware — upgrade / old recommendation
| # | Item | Status | Provenance |
|---|---|---|---|
| 30 | *(ADXL355 — moved to C1#47 SEEN owned)* | was UPGRADE/code-only; DigiKey photos S13 cleared physical-arrival gap | see C1#47 / §B8 |
| 31 | HMC5883L magnetometer | OLD-REC — not the QMC board; never load its driver on QMC5883P | S6 |

### C4) Software (LIST-2025) — SW1–SW10 in §B1 (Bitdefender, Wireshark, ClamAV, UFW, Docker, Bandit, Safety, Python 3, Flask, ROS 2 Humble). None claimed installed on any device.

### C4b) Software — named beyond LIST-2025
| # | Item | Status | Provenance | Open (UNDEF) |
|---|---|---|---|---|
| SW11 | **LocalSend** (cross-platform file share) | SOFTWARE NAMED | S10; Grok share 2026-08-10 iPhone ↔ ASUS TUF A15 ("Fresh Banana") | installed on which devices? |

LIST-2025 SW1–SW10 unchanged (§B1 / prior C4).

### C5) Named but **not counted** as inventory (goals / targets / unclear)
Hive ≥5 drones + optional Queen/Maiden (definition; airframes UNDEF) · braille display, printer (WiFi+BT) — goals · SHILLEHTEK accelerometer (planning C2b#37; vs owned ADXL355 C1#47 — UNDEF) · RP2040, STM32, Rabbit R1 (catalog targets) · small board on jumper bundle (photo, UNDEF) · earbud case engraved "[name masked]" (personal item) · Ghostty (terminal software on A15 share — not hardware) · USB mic (named only in absent Hardware_List.txt summary alongside Camera Module 3).

### C6) Build-merge SUMMARY / DEFERRED / CITED-POSSIBLY (counted; **not** owned evidence)
| # | Item | Status | Provenance | Open (UNDEF) |
|---|---|---|---|---|
| 32 | **Camera Module 3** | LIST-2025 / PLANNING (body) | S11 body HL5 `1964bf2e31c79d4a`; was SUMMARY-ONLY before body fetch | bought?; vs C2#26 Pi Camera Module; vs STATED 2× cam/mic |
| 33 | **NEO-6M GPS** (Pi 5 add-on) | DEFERRED | S10; Gmail 2025-05-07 | purchased later? |
| 34 | **T-Cobbler / PiGPIO** | SUMMARY-ONLY | S10; Gmail 2025-04-21 `196592c54cef81ac` | which cobbler SKU; owned? |
| 35 | **Jetson Nano / Orin Nano** | CITED-POSSIBLY | S10; voice 2026-09-21 "possibly"; share 2026-07-08 | which SKU; owned? |

### C7) Process names (not hardware units)
| # | Item | Status | Provenance |
|---|---|---|---|
| P1 | DigiKey **SVCT-DK-101583476** / SO **101583476** | **ORDER LINE EARNED** for EVAL-ADXL355Z (qty 1) | S13 DigiKey label; was PROVISIONAL_PENDING_RECEIPT (S10). Other DigiKey SKUs still UNDEF. |
| P2 | DigiKey Inventory Update (pinned thread) | NAME ONLY · body UNREACHABLE | S9/S10 |

Quectel EC25 remains C2#29 (LIST-2025; ownership UNDEF).

---

## D) Counts
| Bucket | Count |
|---|---|
| Distinct hardware lines (C1+C2+C3+C6) | **35** (ADXL355 moved C3→C1; no new distinct line) |
| — owned evidence (SEEN / STATED / NAMED-IN-HAND / ACTIVE-POC) | **18** (was 17; **+1** ADXL355 EVAL board; physical units ≥19: cameras ×2) |
| — 2025 planning list only (C2) | **12** — unchanged |
| — upgrade / old-rec (C3 active) | **1** (HMC5883L only; ADXL355 vacated) |
| — SUMMARY / DEFERRED / CITED-POSSIBLY (C6) | **4** (Camera Module 3, NEO-6M, T-Cobbler, Jetson) |
| Distinct software lines (LIST-2025 + LocalSend) | **11** |
| Process names (C7) | **2** (P1 now order-line-earned for ADXL355) |
| **Total distinct as-found HW+SW items** | **46** (no Δ — S12#46 merged into C1#47) |
| 2025 Gmail rows parsed | 24 (×3 identical copies) + 12-line docx subset (×2) |
| Items in 2025 list later confirmed SEEN | 1 (MPU-6050 → GY-521); Pi 5 NAMED-IN-HAND |
| Actual costs found | **1 STATED approx** — DigiKey ADXL355 ~$90 after packaging/shipping (few bucks back); SKU now earned |
| DigiKey order lines found | **1** — PN **505-EVAL-ADXL355Z-ND** qty 1 · SO **101583476** · INV **[INV masked]** · 13-SEP-2026 15:23 |
| Not counted (C5 goals/targets/unclear) | ~10 names |

Key categories (hardware 35): compute hosts **4** owned-evidence + **1** Jetson CITED-POSSIBLY · motion/heading **6** (incl. owned ADXL355) · power/environment **5** · ranging **2** + **1** NEO-6M DEFERRED · vision/audio **4** + **1** Camera Module 3 SUMMARY · display/input **5** · storage/cables **4** · connectivity **1** Quectel EC25 · GPIO accessory **1** T-Cobbler SUMMARY · unknown **1** black vented case. (Category sketch only; sum of sketches may overlap LIST vs SUMMARY naming.)

**Delta 2026-10-05 Hardware_List body + accelerometer (S12):** S11 body on box · + HL planning rows (HiLetgo voltage module, SHILLEHTEK accel, USB mic/speaker, 2.8 TFT, 1TB SSD, DHT22, air quality, Pi 5 cluster, 128GB+ microSD) · + better **accelerometer** DigiKey ~$90 after pkg/ship (few $ back), STATED/pending pro solder (model/SKU UNDEF) — Timothy correction: not altimeter · Camera Module 3 upgraded from SUMMARY-ONLY to body-cited PLANNING · archive-not-delete standing locked.

**Delta 2026-10-05 ~7:01 PM ET — S12 correction:** Timothy meant **accelerometer** not altimeter. DigiKey ~$90 after packaging/shipping; few bucks back; unsoldered for pro solder; model/SKU was UNDEF then.

**Delta 2026-10-05 ~7:05 PM ET — S13 DigiKey ADXL355 lock:** Photos lock PN **505-EVAL-ADXL355Z-ND** / MFR **EVAL-ADXL355Z** / SO **101583476** (= SVCT-DK-101583476) / INV **[INV masked]** / bag S/N **[S/N masked]** / date **13-SEP-2026 15:23**. Merges S12 + former C3#30 → **C1#47 SEEN owned**. DigiKey order-line gap **cleared for this part**. Boot `0.70710678` OK. Prior archived. No GitHub.

**Delta this Build merge:** + Camera Module 3 · + NEO-6M · + T-Cobbler/PiGPIO · + Jetson (elevated from uncounted C5) · + LocalSend · ADXL355 notes enriched · Pi Zero date confirmed 2025-10-03 · DigiKey SVCT process name recorded · Quectel EC25 unchanged.

---

## E) Gaps (fail-closed)
1. **DigiKey Inventory Update** — pinned Grok thread name only; body not on box, local DigiKey inventory file gone, Notion "DigiKey" = 0. **PARTIAL CLEAR:** SO **101583476** / SVCT-DK-101583476 now has **one earned order line** from label photo (S13): PN **505-EVAL-ADXL355Z-ND** qty 1, INV **[INV masked]**, 13-SEP-2026 15:23. Cost ~$90 STATED (S12). **Other DigiKey SKUs / full invoice lines still UNDEF.**
2. **Private X / signed-in Grok sessions** (`@Tnorman01775634`) — blocked (box browser logged out; last logged-out read "Account suspended"). Inventory threads from ~1½–2 years back that live only there are **not reached**.
3. **Share Catalog** — `/workspace/share-catalog/` left **sealed**; not used as a hardware source.
4. **What was actually bought in April 2025** — "First Order Raspberry Pi kit +" attachment is the same planning list; no receipts / order confirmations among the five messages; "Actual Cost" column empty.
5. **Ownership of 12 LIST-2025 items** (battery, BMS, DHT11, HC-SR04, ACS712, voltage, LIDAR, Pi Camera, OLED, VR goggles, microSD, Quectel EC25) — UNDEF.
6. **ADXL355** physical presence — **CLEARED (SEEN)** via DigiKey label + Analog Devices box/bag photos (S13). Still open: professional solder; host wiring; fresh bus scan; POC bind ticket. **SHILLEHTEK** relation to ADXL355 still UNDEF (planning only). Driver evidence: ETMR 48/48 + prior `i2cdetect` **1d**; `pi_adxl355_link.py` body empty locally.
7. **Bus scan** — no fresh `i2cdetect -y 1` earned this sitting; GY-521/QMC addresses remain ASSERTED typical; ADXL355 **1d** is prior cite only.
8. **Photo unknowns** — black vented case with green light; small board on jumper bundle; webcam/camera models; Pi Zero 2 W setup state.
9. Session-map `session-map-2026-09-14-pi5-grokcli-adxl` local bytes gone; GitHub code search for DigiKey/ADXL355 returned incomplete results (not re-run; GitHub out of scope this pass).
10. Sealed kbld / MinRadius / GOSUB bodies — excluded by standing rule.
11. **Hardware_List.txt** (2025-04-18) — **body now on box** (`1964bf2e31c79d4a` → `inventory-gmail-2025/Hardware_List_body_1964bf2e31c79d4a.txt`). Still **planning only** (no purchase evidence). Prior "file ABSENT" gap closed for body text.
12. **NEO-6M / T-Cobbler** — Gmail summary cites only; purchase/ownership UNDEF.
13. **Jetson Nano / Orin Nano** — "possibly" wording; not photo-confirmed.
14. **LocalSend** — share describes use; install state on phone/laptop UNDEF.

## F) Do-not-invent (carried)
No quantities beyond those stated (JBL 1×, cameras 2×, Hive ≥5 definition, ADXL355 eval qty 1). No prices paid **except** S12 DigiKey ~$90 after pkg/ship (few $ back) as Timothy STATED — still not a printed price on the label. DigiKey ADXL355 SKU/SO/INV **earned from photos** (S13); do not invent other DigiKey lines. S12 ≡ C1#47 ADXL355 (merged). No Quectel SKU beyond "EC25" as written in Timothy's 2025 list. No fresh I2C results this sitting. No pairing. Catalog targets ≠ owned. BMM150 not merged into the 2026-09-21 POC table. HMC driver never on QMC. ADXL355 still not POC floor until bind ticket VAL's.

## Footer
| Item | Value |
|---|---|
| Parser | python3 + openpyxl + python-docx (already present on box; no venv needed) |
| Gmail access | read-only `get_thread` on 6 ids; nothing sent, labeled, or modified |
| Sources modified | holdings Pi Zero date corrected; this file + MASTER; Build report read-only; S11 Hardware_List body; S12→S13 DigiKey ADXL355 lock (photos + inventory); APPEND_ARCHIVE standing |
| GitHub push (inventory) | **SKIPPED** this ADXL355 lock |
| Publish | **NO** |
| Share Catalog | **sealed** |
