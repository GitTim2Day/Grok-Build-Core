# Session pattern map — evidence fusion, not identity

Stamp: 2026-10-08T12:16-04:00
Lane: build-shelves. One start. Not a second project.
Sibling of the face-geometry prototype sitting the same morning. Not a merge.
Owner: Timothy. Mask first. No identity claim. No patient record. No photograph in this file.

## Line

Pattern, match, and map the multimodal evidence proposition. Add it to the project. Record capture only. The fusion engine is not built.

## Pattern

One photograph, one radiograph, or one facial formula does not establish identity.
Every observation contributes to one geometric and contextual record.
No separately programmed workflow for every pairing of evidence.

Sources named: facial photograph, dental image, CT, PET, skeletal measurement, medical record.
KBLD9 gate: validate, timestamp, provenance, units, reject malformed.
SVCT store: landmarks, tooth surfaces, bone contours, ratios, 3D relations.
UDN: use on detection of need. Select the primitive the evidence actually requires. Register views. Compare. Invoke a specialist only then.
Fusion review: consistency, contradiction, uncertainty, expert stop.

Dental table is a representation map, not a match score.

| Evidence | Representation |
| --- | --- |
| Tooth shape | Contours, curvature, surface geometry |
| Tooth position | Coordinates, spacing, orientation |
| Fillings and crowns | Region geometry and material or intensity difference |
| Root configuration | Branching curves and angular relations |
| Jaw structure | Connected curves and 3D surfaces |
| Multiple viewpoints | Registration and projection transforms |

PET is tracer distribution. It is not equivalent anatomy. CT can yield surfaces from intensity. A photograph is a 2D projection until another view or a prior supplies depth.

Two measurements stay split:
- Anatomical consistency: how closely the structures in hand agree.
- Identity confidence: how well that agreement separates one person from others who could have produced it.

A similarity score is not an identity probability. 70–80% is not assigned. That figure needs a reference population, known matches, known non-matches, and a measured error rate. None of that has been run. Forensic use keeps the expert and the confirmatory procedure. This chair does not issue an identification.

## Match

Face prototype in hand this sitting. Independent. Does not identify a person. Does not edit the KBLD9 kernel.
Script SHA-256 43cafe098361ca788f347fb8764ae1b60f3c75e43d78c4c6f288ea2fba51fd71. 56 lines. Parse holds.
Stored ratio design is an integer fraction: eye-center horizontal separation / detected face width. No rounding in the stored ratio.
Its own limitations block already says: Haar boxes are not landmarks, curves are handwritten, 2D only, no identity test, no 64-cell encoding, no contour ground truth.
UDN names the same dispatch-on-need seam already used in the curation path. The fusion engine is not that seam.
KBLD9 gate matches the existing validate / timestamp / provenance / reject rule. It does not become a recognizer by being placed in front of images.

## Map

| Rung | State |
| --- | --- |
| Proposition received | HIT |
| Identity withheld | HIT |
| 70–80% not assigned | HIT |
| Script parse | HIT |
| Script run | VAL fail. Exit 1. Source JPEG absent. |
| Overlay, primitives, source hash | miss |
| Fusion engine | not built |
| Calibrated identity rate | not run |
| Next cut, only if named | one observation record (modality, units, timestamp, source hash, uncertainty) plus a second record, then a registration that reconciles or flags the contradiction |

## Runs

First run: `ModuleNotFoundError: No module named 'cv2'`.
Declared fix, not a package named cv2: `python3 -m pip install opencv-python-headless pillow`.
Second and third runs, after install on this seat (`cv2` 5.0.0, Pillow 12.3.0): OpenCV cannot open `/mnt/data/IMG_46DAC99A8E6B-1.jpeg`. `imread` returns None. Line 8: `AttributeError: 'NoneType' object has no attribute 'shape'`. Exit 1.
`/mnt/data` does not exist on this seat. Attachment was the `.py` only. Drive title search for `IMG_46DAC99A8E6B-1.jpeg` and `46DAC99A8E6B` returned no file. No substitute image was generated.

## HIT / VAL / miss / open

- HIT: proposition mapped; identity split held; script parsed; import failure then image failure both shown.
- VAL: record only. No geometry file written. No cross-modality registration. No error rate.
- miss: source JPEG not in hand. Yahoo CC on this hop is verified only after the sent message is fetched.
- open: fusion pair not started. Do not start it from this map.

## Shelves

Hop first. Notion Timothy Skills & KB. GitHub GitTim2Day/Grok-Build-Core/knowledge. Drive Grok_Build_Archives_2026. Local pointer after the hop message_id.
Ledger 1a11c4db08df1156.
BOOT ≠ SAVE.
