#!/usr/bin/env python3
# three_channel_intake.py
# No sudo. String only. Shared America/New_York timestamp.
# Identical contract for Python / C++ / BASIC.

from datetime import datetime
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")

def stamp_now():
    # Fixed-format timestamp, America/New_York
    return datetime.now(NY).strftime("%Y-%m-%dT%H:%M:%S.%f")[:26] + "-04:00"

def capture_three(speech_frag="", ocr_frag="", motor_line=""):
    """Capture three string channels under one shared timestamp.
    Empty string after strip marks a failed channel.
    Returns: (channels_dict, failed_list, timestamp)
    """
    ts = stamp_now()
    speech = speech_frag.strip() if speech_frag is not None else ""
    ocr    = ocr_frag.strip()    if ocr_frag    is not None else ""
    motor  = motor_line.strip()  if motor_line  is not None else ""

    channels = {
        "speech": {"ts": ts, "text": speech},
        "ocr":    {"ts": ts, "text": ocr},
        "motor":  {"ts": ts, "text": motor},
    }
    failed = [name for name, ch in channels.items() if not ch["text"]]
    return channels, failed, ts
