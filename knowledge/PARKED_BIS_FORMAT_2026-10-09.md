# PARKED — .bis file format (decision 2026-10-09)

Stamp: 2026-10-09T00:00-04:00
Owner: Timothy ("Log it or archive it, and we'll come back to it if we need it."). Seat: Claude. Append only.
Status: PARKED. Nothing built. Reopen on first contact with a real .bis file.

## Question
Timothy: ".bis is another file format." Which one is closest to our work, and is it worth building?

## Search path (reproducible)
- Repo grep for `.bis` / "BIS format": NOT FOUND. Past chats ("bis file format frames"): NOT FOUND.
- Web search ".bis file extension format", then the pages below. Five unrelated formats share the extension.

| # | Format | What it is | Source |
| --- | --- | --- | --- |
| 1 | bis compressor | C tool, Burrows-Wheeler + Huffman; binary, starts with `42 49 53` ("BIS"); `x` -> `x.bis` | https://github.com/cifkao/bis/wiki/Documentation (no license seen) |
| 2 | Kst-plot BIS | image-frame stream (astronomy camera work, C. Barth Netterfield, U of Toronto); 2x uint16 header (type 0xE6B0, frame size), frames of 5 x 8-bit images with width/height/x/y; host byte order | https://lxr.kde.org/source/graphics/kst-plot/src/datasources/bis/bis.c (GPL v2+) |
| 3 | BeInSync | rename wrapper (`doc.doc.bis`), discontinued Phoenix Technologies sync tool | https://www.file-extensions.org/extension/bis |
| 4 | QMF for Workstation | IBM query tool listed as an opener; no published layout | https://file.org/extension/bis |
| 5 | Timothy's own | if he defined one, its layout lives in his notes | — |

## Pick, if ever needed
#2 Kst-plot BIS is the closest to our work (Canvas RGB frame player, Pi 5 Vision channel cameras, earlier DICOM/voxel frames).
Gaps against the canon: no magic/version, host byte order, 16-bit frame size (max 65,535 bytes), fixed 5 images, 8-bit mono, no time/units/hash.
If reopened: (a) a reader for real Kst BIS written from the published layout (not their GPL code); (b) optionally our own write
variant = magic + version + declared byte order + per-frame time, units, scale + SHA-256 chain (SVCT around frames).

## Why parked (right-size rule)
- Nothing we have produces or receives .bis; the kit already has a frame format (base64 raw RGB in JSON) and SVCT carries hash/time/provenance.
- #1 duplicates bzip2, which IS Burrows-Wheeler + Huffman: Python `bz2` (stdlib, every device), Raspberry Pi OS, and the TXT->RCRJ door already reads .bz2.
- A Kst BIS reader is about a page of code; build it against a real file when one arrives.

## Standing practice adopted instead
Archive SVCT records with bzip2 and keep the SHA-256 of the uncompressed bytes.
