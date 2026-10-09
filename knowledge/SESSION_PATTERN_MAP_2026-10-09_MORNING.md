# Session pattern map — 2026-10-09 morning (07:30–08:40 ET)

Owner: Timothy. Seat: Claude. Append only. Public half only; personal items are in the private archive.
Each row: the pattern, where it showed up, the rule it leaves behind. Labels: EARNED (run and checked this session), PROPOSED.

| # | Pattern | Where it showed up | Rule left behind | Label |
| --- | --- | --- | --- | --- |
| 1 | Stop boundary untested | base-360 converter: `>` → `>=` passed all 11 original tests | Every stop rule gets an equality test, a one-step-tighter test and a budget test; then mutate the comparison | EARNED (21/21, 9/9 mutants) |
| 2 | Negative zero in display | base-360 `format_digits` printed `-0.000` for small negatives | Record keeps sign and exact error; display drops the sign when every shown digit is zero | EARNED (leaf, original untouched) |
| 3 | Copy beside its own unpacked members | two zips committed next to their contents | README: binaries live on Drive, one unique copy; unpack text, record zip hashes, keep zips off the public tree | EARNED (correction ce2b32a) |
| 4 | Personal data in a public tree | intake had face, household and device-identifying items | Split before commit: code and tests public; faces, homes, devices, contacts, IDs private; grep the fresh public clone for private markers | EARNED |
| 5 | Pick files without asking | many repos, Drive, archive | `scripts/file_map_2026-10-09.py`: one row per file (path, bytes, SHA-256, kind, how to test) | EARNED |
| 6 | Hand-placed points sold as detection | face script: outline and features placed by hand, only eyes detected | Label hand-placed vs detected on every point; overlay the drawing on its claimed source to prove which photo it came from | EARNED |
| 7 | Search that wins at its own edge | symmetry axis/tilt search landed on range limits | Fixed window; mirrored-image control must score 0 at centre; flag any result on a search boundary as not trusted | EARNED (method), NOT EARNED (verdicts) |
| 8 | Real vs generated | photos, screenshots, a generated video | File evidence first (camera EXIF, generator tags, file name); appearance only as ASSERTED; screenshots carry no proof | EARNED for the video only |
| 9 | Contact details asked again and again | appointments, people, offices | Contact path: calendar event fields → vCard export (`scripts/vcf_to_jsonl_2026-10-09.py`) → linked computer / Pi CardDAV with permission → official site by web search for businesses → ask Tim. People-search sites never close a fact | EARNED (parser 15/15, 7/7 mutants) |
| 10 | Old registry number reused as a secret | a number still printed on a public registry was in use as a password | Never store credentials; warn when a secret equals any public identifier | EARNED |
| 11 | Re-check with the cleaner source | identity fields | Rank 2 (official registry, retrieved now, with last-update date) checks rank 4–6 claims; record MATCH per field | EARNED |

## Not done this morning
Landmark face detector on the Pi/A15 (model file blocked here); C++ for base-360 and UDN; contacts route on a device.
