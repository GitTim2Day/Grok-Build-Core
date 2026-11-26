# Private Connecter (TER) — Initial Destinations

**Status:** Not a TOR. Private only. Trial on his machine.

## Initial shareable destination: Box

Box is already connected. Shareable photos or OCR text can go there first.

- Text/OCR results: use the connected Box upload tool (text content).
- Binary photos: Box requires the get_upload_url path for non-text files. The local subroutine prepares the file and hands the upload to the already-authorized Box connector.
- Private files never leave the Pi 5, A15, or 2 TB drive.

## Later optional path: iCloud Drive

1. On Shepherd or A15: `pip install pyicloud` (unofficial).
2. Login once interactively. Session cookiejar stays local.
3. Local only. No public URL. Human gate for any write.

## Boundary

- TER: local decision + local subroutine. User control.
- Shareable → Box (initially). Private → device or 2 TB.
- TOR: public custom MCP. Requires explicit approval. Not built.
