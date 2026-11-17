# Session Pattern Map — 2026-11-17 Pi 5 OCR 1080p Continuation

**Stamp:** 2026-11-17T09:54:27-05:00 America/New_York (EST)  
**Seat:** shepherd@raspberrypi:~/vosk (Pi 5)  
**Sibling of:** SESSION_PATTERN_MAP_2026-11-05_PI5_VOICE_OCR_PASS2.md, not a merge.  
**Prior:** eng + spa confirmed no-sudo; 640×480 frame too small; v4l2 vs 412 font trap identified.

## Pattern Match

- Goal locked: 1080p capture then Tesseract OCR on eMeet C960 (/dev/video0).
- Paper discipline: fold so only print is in frame; dark clear text preferred.
- Camera source: eMeet (not iPhone selfie — selfie reverses print).
- Intermediate text path: OCR text → local library (same as speech path) → optional UT translate → Piper → JBL sink 96.
- Terminal font trap remains: digit 1 has flag, lowercase L is plain stick. v4l2 is vee-four-ell-two.
- No-sudo holds. All under ~/vosk. TESSDATA_PREFIX and binary already confirmed.
- Time discipline: America/New_York, fresh checks.

## Map

1. User returned with sheet photos (folded bottom, print only).
2. Prior capture estimated resolution ~328–1237; text not readable by Tesseract.
3. Corrected command given and emailed (Yahoo + Gmail):
   ffmpeg -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video0 -frames:v 1 -update 1 -y page.jpg && ./tesseract page.jpg page -l eng && cat page.txt
4. User typed manually with ell, still saw errors (device open / format).
5. Light flash idea noted (3 flashes before capture) for later.
6. Live stream watch via ffplay confirmed as possible for framing.
7. Resolution target: 1920x1080 mjpeg for OCR viability on half-letter sheet.

## Audit

- HIT: eng/spa listed; prior page.jpg existed; fold-and-isolate method stated; 1080p command prepared and emailed; font trap reconfirmed.
- VAL: languages confirmed earlier; email delivery worked (user saw it on phone and Pi mail).
- miss: 1080p frame not yet successfully captured this sitting; OCR text still not produced; library write not wired.
- open: execute the 1080p line on shepherd; confirm page.jpg size and Tesseract output; save text to local library.

## Pattern Match Again

The seat that uses the result is the Pi 5 terminal under ~/vosk. Commands it can run are already on the machine. The 1080p line is the next executable step. Intermediate text stays local. Full UT and independent models stay on A15. Do not lead with what the page cannot do.

## Copy-paste resume block (1080p OCR)

```bash
cd ~/vosk
ffmpeg -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video0 -frames:v 1 -update 1 -y page.jpg && ./tesseract page.jpg page -l eng && cat page.txt
```

If device busy or format rejected, first:
```bash
ffplay -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video0
```
(q or X to close). Then retry capture.
