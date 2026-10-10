---
name: pi5-usb-camera-ocr
description: "Raspberry Pi 5 USB camera OCR text extraction with OpenCV and Tesseract. Use for eMeet C960 or other UVC webcams on Pi 5, ROI cropping, real-time bounding boxes, and offline text extraction."
type: workflow
lifecycle: active
---

# Pi5 USB Camera OCR

Offline OCR from USB camera (eMeet SmartCam C960 UVC or similar) on Raspberry Pi 5. Uses OpenCV for capture/preprocess and Tesseract via pytesseract. Triggered or continuous modes. Center or fixed ROI recommended for performance.

## Confirm Camera

```bash
ls -l /dev/video*
v4l2-ctl --list-devices
ffplay -f v4l2 -i /dev/video0   # q to close
# sharper: ffplay -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video0
```

## Install (Bookworm 64-bit)

```bash
sudo apt update
sudo apt install -y tesseract-ocr libtesseract-dev python3-opencv python3-pip python3-venv
python3 -m venv ~/ocr-venv
source ~/ocr-venv/bin/activate
pip install pytesseract
```

Confirm: `tesseract --version` and `python3 -c "import cv2; print(cv2.__version__)"`.

## Minimal Triggered OCR

```python
#!/usr/bin/env python3
import cv2
import pytesseract

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("Press 's' to OCR, 'q' to quit")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("USB Camera OCR", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
        text = pytesseract.image_to_string(thresh, config="--psm 6")
        print("--- OCR ---\n" + (text.strip() or "(empty)") + "\n-----------")
cap.release()
cv2.destroyAllWindows()
```

## ROI Cropping

Center crop (recommended first):

```python
def crop_roi(frame, margin=0.2):
    h, w = frame.shape[:2]
    y1, y2 = int(h * margin), int(h * (1 - margin))
    x1, x2 = int(w * margin), int(w * (1 - margin))
    return frame[y1:y2, x1:x2], (x1, y1)
```

Fixed or interactive: `cv2.selectROI` once, then hard-code coordinates. Always OCR the cropped ROI, not the full frame.

## Real-time Bounding Boxes

```python
from pytesseract import Output

data = pytesseract.image_to_data(thresh, output_type=Output.DICT)
for i in range(len(data["text"])):
    if int(data["conf"][i]) > 60 and data["text"][i].strip():
        x = data["left"][i] + offset[0]
        y = data["top"][i] + offset[1]
        w, h = data["width"][i], data["height"][i]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, data["text"][i], (x, y - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
```

## Combined Script (center ROI + live boxes + key print)

See full version in previous session response or regenerate from the fragments above. Continuous OCR is CPU-bound; prefer triggered or interval + ROI.

## Notes

- C960 is fixed-focus UVC. Keep text in sharp zone; lighting and contrast dominate accuracy.
- Confidence filter >60; try `--psm 6` or `11`.
- For higher throughput: tighter ROI, downscale, or alternative engines (EasyOCR / PaddleOCR-Lite).
- Provenance: stamp extractions with timestamp + frame hash if integrating with Shepherd/KBLD.
