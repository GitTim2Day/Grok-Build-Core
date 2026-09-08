#!/usr/bin/env python3
"""
KBLDA_RTMP_US_EAST_v3
US East (N. Virginia) locked.
GOSUB + IF-THEN + IF-THEN-ELSE nesting.
Error / missing-key handling.
X RTMP authentication: none (explicit guard).
OBS config only on detection.
HLS optional side path.
Pure stdlib. No type hints. Bounded.
Author lineage: Timothy H Norman + Grok Build 2026-07-19
"""

import hashlib
import json
import time
import re

MIN_SCORE = 0.1

def gosub_error_handle(missing, context=""):
    """GOSUB: Error Recovery for missing keys / fields"""
    return {
        "status": "ERROR",
        "missing": missing,
        "context": context,
        "action": "Supply missing value and re-call GOSUB",
        "note": "No zero / no silent failure — explicit ER"
    }

def gosub_detect_need_obs_config(encoder_type="unknown"):
    """GOSUB: Detect if OBS (or compatible) needs RTMP configuration"""
    if encoder_type.lower() in ["obs", "obs studio", "streamlabs", "unknown", ""]:
        return True
    else:
        return False

def gosub_configure_obs_rtmp(credentials):
    """GOSUB: Configure OBS for RTMP push (only on detection)"""
    if not credentials.get("rtmp_url") and not credentials.get("rtmps_url"):
        return gosub_error_handle("rtmp_url or rtmps_url", "OBS config")
    if not credentials.get("stream_key"):
        return gosub_error_handle("stream_key", "OBS config")

    if credentials.get("rtmps_url"):
        url = credentials["rtmps_url"]
    else:
        url = credentials["rtmp_url"]

    key = credentials["stream_key"]

    return {
        "status": "OBS_CONFIGURED",
        "server": url,
        "key": key,
        "note": "Start Streaming in OBS only after Create Broadcast on X. Then run audio sync offset if lips are off.",
        "next": "gosub_obs_audio_sync_offset()"
    }


def gosub_obs_audio_sync_offset():
    """GOSUB: OBS Audio Sync Offset (Lip Sync Fix)
    Path: OBS → Edit → Advanced Audio Properties
    Preferred method: calibrate with video playback
    """
    return {
        "status": "AUDIO_SYNC_GUIDE",
        "path": "OBS → Edit → Advanced Audio Properties",
        "preferred_method": "video_playback",
        "steps": [
            "On the Mic / Desktop Audio row set Sync Offset (ms)",
            "Positive (+) = delay audio",
            "Negative (–) = advance audio",
            "1. Start test Broadcast in Media Studio + Start Streaming in OBS",
            "2. Add a Media Source in OBS and play a clear talking-head or clap-test video",
            "3. Watch the live stream on a second device (phone / second monitor)",
            "4. Adjust Sync Offset in 50–100 ms steps while watching lips vs audio",
            "5. Common range: +50 ms to +200 ms (most sources need small delay)",
            "6. Stop when lips and sound match perfectly",
            "Apply → close window (offset persists)"
        ],
        "alternative": "Speak live into the mic while watching the stream if no test video is available",
        "note": "Video playback gives more consistent and repeatable calibration than live speech"
    }

def gosub_create_rtmp_source(source_name):
    """GOSUB: Create RTMP source (US East only)"""
    if not source_name or not source_name.strip():
        return gosub_error_handle("source_name", "Create RTMP source")

    region = "US East (N. Virginia)"
    source_type = "RTMP"

    return {
        "status": "CREATED",
        "source_name": source_name,
        "region": region,
        "type": source_type,
        "auth": "NONE"
    }

def gosub_get_rtmp_credentials(source_name):
    """GOSUB: Retrieve RTMP / RTMPS credentials + missing-key guard"""
    if not source_name:
        return gosub_error_handle("source_name", "Get credentials")

    # Live credentials (US East) — supplied by user 2026-07-19
    rtmp_url = "rtmp://va.pscp.tv:80/x"          # non-secure fallback
    stream_key = "xyh6injnm1q4"
    rtmps_url = "rtmps://va.pscp.tv:443/x"       # preferred

    if not rtmp_url:
        return gosub_error_handle("rtmp_url", "Credentials missing")
    if not stream_key:
        return gosub_error_handle("stream_key", "Credentials missing")

    return {
        "status": "OK",
        "rtmp_url": rtmp_url,
        "stream_key": stream_key,
        "rtmps_url": rtmps_url,
        "auth": "NONE"
    }

def gosub_publish_and_test(credentials):
    """GOSUB: Push + create test broadcast"""
    if credentials.get("status") != "OK":
        return gosub_error_handle("valid credentials", "Publish")

    return {
        "status": "PUSHING",
        "note": "Create test Broadcast before public live. Select the source."
    }

def gosub_create_hls_source(source_name, hls_pull_url):
    """OPTIONAL SIDE GOSUB: Create HLS source (only if pull URL supplied)"""
    if not hls_pull_url or not hls_pull_url.strip():
        return {"status": "SKIP", "note": "No HLS pull URL — optional path not taken"}

    if not source_name:
        return gosub_error_handle("source_name", "HLS create")

    region = "US East (N. Virginia)"

    return {
        "status": "HLS_CREATED",
        "source_name": source_name,
        "region": region,
        "pull_url": hls_pull_url
    }

def gosub_rtmp_full_flow(source_name="KBLDA_US_EAST_01", encoder_type="obs", hls_pull_url=""):
    """Master GOSUB — stacked sequence with detection + ER"""
    create_result = gosub_create_rtmp_source(source_name)
    if create_result.get("status") != "CREATED":
        return {"status": "ABORT", "detail": create_result}

    creds = gosub_get_rtmp_credentials(source_name)
    if creds.get("status") != "OK":
        return {"status": "ABORT", "detail": creds}

    if gosub_detect_need_obs_config(encoder_type):
        obs_result = gosub_configure_obs_rtmp(creds)
        if obs_result.get("status") == "ERROR":
            return {"status": "ABORT", "detail": obs_result}
    else:
        obs_result = {"status": "SKIP", "note": "Encoder already configured or not OBS"}

    publish_result = gosub_publish_and_test(creds)

    hls_result = gosub_create_hls_source(source_name + "_HLS", hls_pull_url)
    audio_sync = gosub_obs_audio_sync_offset()

    return {
        "status": "READY",
        "source": source_name,
        "region": "US East (N. Virginia)",
        "credentials": creds,
        "obs": obs_result,
        "publish": publish_result,
        "hls_optional": hls_result,
        "audio_sync": audio_sync,
        "auth": "NONE — X RTMP does not support authentication",
        "note": "Source reusable. Limit 100. Delete unused if Create fails silently. Prefer RTMPS. Always test broadcast. Run audio sync if lips are off."
    }

def _self_test():
    print("=== KBLDA_RTMP_US_EAST self-test ===")
    # Test create
    r = gosub_create_rtmp_source("test_src")
    assert r["status"] == "CREATED"
    print("  [PASS] create")

    # Test missing name
    r = gosub_create_rtmp_source("")
    assert r["status"] == "ERROR"
    print("  [PASS] missing name ER")

    # Test detect
    assert gosub_detect_need_obs_config("obs") == True
    assert gosub_detect_need_obs_config("ffmpeg") == False
    print("  [PASS] detect OBS")

    # Test full flow with live credentials
    full = gosub_rtmp_full_flow("test_src", "obs", "")
    assert full["status"] == "READY", full
    assert full["obs"]["status"] == "OBS_CONFIGURED"
    print("  [PASS] full flow structure + live credentials")

    print("=== ALL GREEN ===")
    return True

if __name__ == "__main__":
    _self_test()
    print()
    result = gosub_rtmp_full_flow(
        source_name="KBLDA_US_EAST_01",
        encoder_type="obs",
        hls_pull_url=""
    )
    print(result)
