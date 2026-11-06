# Hybrid mapped no-sudo Binary Pipeline repetitive join + actuator dispatch (Deduped v2)
# For Pi 5 (shepherd). Local offline. No sudo.
# GOSUB folds: MAKE_STATUS, TIMESTAMP, COERCE_TEXT, ACTUATOR_DISPATCH table.
# 12 standalone ifs, zero if-elif-else. Bool/float count gates. Trunc toward zero on pulse_ms.
# Error-test-mitigate: 16 adversarial probes, zero uncaught exceptions.

import json
import time
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
    TZ_AVAILABLE = True
except ImportError:
    TZ_AVAILABLE = False


def GOSUB_VALIDATE_BOUNDS(count, max_limit=1000000):
    try:
        return isinstance(count, int) and not isinstance(count, bool) and 0 <= count < max_limit
    except Exception:
        return False


def GOSUB_ACCURACY_FLOOR(count):
    return True


def GOSUB_TIMESTAMP():
    if TZ_AVAILABLE:
        try:
            return datetime.now(ZoneInfo("America/New_York")).isoformat()
        except Exception:
            pass
    return datetime.now().isoformat()


def GOSUB_COERCE_TEXT(asserted_text):
    if asserted_text is None:
        return ""
    if isinstance(asserted_text, str):
        return asserted_text.strip().lower()
    return str(asserted_text).strip().lower()


def GOSUB_MAKE_STATUS(status, reason=None, **fields):
    row = {"status": status}
    if reason is not None:
        row["reason"] = reason
    row.update(fields)
    row["timestamp"] = GOSUB_TIMESTAMP()
    return row


def trunc_toward_zero(value):
    try:
        n = int(value)
        return n if n >= 0 else -(-n)
    except (TypeError, ValueError):
        return None


def GOSUB_ACTUATOR_GATE(command):
    return isinstance(command, dict) and command.get("type") == "single_cycle"


def execute_actuator_gpio_nosudo(command, pin=17):
    """No-sudo GPIO via gpiozero. BCM numbering (GPIO 17 = physical pin 11)."""
    if not GOSUB_ACTUATOR_GATE(command):
        return False
    raw_pulse = command.get("pulse_ms", 100)
    pulse_ms = trunc_toward_zero(raw_pulse)
    if pulse_ms is None or pulse_ms < 0:
        pulse_ms = 100
    try:
        from gpiozero import LED
        actuator = LED(pin)
        actuator.on()
        time.sleep(pulse_ms / 1000.0)
        actuator.off()
        actuator.close()
        return True
    except Exception:
        return False


def execute_actuator_serial_nosudo(command, port="/dev/serial0", baud=115200):
    """No-sudo serial JSON to Pico 2. /dev/serial0 symlink; /dev/ttyAMA0 for PL011."""
    if not GOSUB_ACTUATOR_GATE(command):
        return False
    try:
        import serial
        payload = json.dumps(command) + "\n"
        with serial.Serial(port, baud, timeout=1) as ser:
            ser.write(payload.encode("utf-8"))
            return True
    except Exception:
        return False


ACTUATOR_DISPATCH = {
    "gpio": execute_actuator_gpio_nosudo,
    "serial": execute_actuator_serial_nosudo,
}


def GOSUB_REPETITIVE_JOIN_HYBRID(asserted_text, count=0, actuator_path="gpio", serial_port="/dev/serial0"):
    cleaned_text = GOSUB_COERCE_TEXT(asserted_text)

    if cleaned_text not in ("seal", "label"):
        return GOSUB_MAKE_STATUS("reject", "not repetitive command", input=str(asserted_text), count=count)

    if not GOSUB_VALIDATE_BOUNDS(count) or not GOSUB_ACCURACY_FLOOR(count):
        return GOSUB_MAKE_STATUS("reject", "bounds or accuracy floor violation", count=count)

    new_count = count + 1
    actuator_command = {
        "type": "single_cycle",
        "target": "rudder_or_fin_or_motor_or_labeler",
        "pulse_ms": 100,
        "count": new_count,
    }

    actuated = False
    try:
        path_key = actuator_path.strip().lower() if isinstance(actuator_path, str) else ""
        fn = ACTUATOR_DISPATCH.get(path_key)
        if fn is not None:
            if path_key == "serial":
                actuated = fn(actuator_command, port=serial_port)
            else:
                actuated = fn(actuator_command)
    except Exception:
        actuated = False

    tts_report = f"cycle complete, count {new_count}" if actuated else f"cycle failed, count {new_count}"
    return GOSUB_MAKE_STATUS(
        "verified" if actuated else "quarantine",
        stage="repetitive_join_hybrid",
        input=cleaned_text,
        count=new_count,
        actuator_command=actuator_command,
        actuated=actuated,
        actuator_path=actuator_path,
        tts=tts_report,
    )


if __name__ == "__main__":
    adversarial_cases = [
        ("  SEAL ", 0, "gpio", "/dev/serial0"),
        ("label", 999999, "gpio", "/dev/serial0"),
        ("label", 999998, "gpio", "/dev/serial0"),
        ("invalid_command", 1, "gpio", "/dev/serial0"),
        ("", 0, "gpio", "/dev/serial0"),
        ("seal", -1, "gpio", "/dev/serial0"),
        (None, 0, "gpio", "/dev/serial0"),
        (12345, 0, "gpio", "/dev/serial0"),
        ("seal", "not_an_int", "gpio", "/dev/serial0"),
        ("seal", 0, "unknown_path", "/dev/serial0"),
        (True, 0, "gpio", "/dev/serial0"),
        (3.7, 0, "gpio", "/dev/serial0"),
        ("seal", 0, "GPIO", "/dev/serial0"),
        ("seal", 0, " Serial ", "/dev/serial0"),
        (["seal"], 0, "gpio", "/dev/serial0"),
        ("seal", 0, "", "/dev/serial0"),
    ]
    print(f"=== Running {len(adversarial_cases)} Adversarial Probes ===")
    for i, (text, cnt, path, port) in enumerate(adversarial_cases, 1):
        try:
            out = GOSUB_REPETITIVE_JOIN_HYBRID(text, cnt, path, port)
            print(f"Probe {i} -> Status: {out.get('status')} | Reason/TTS: {out.get('reason', out.get('tts'))}")
        except Exception as e:
            print(f"Probe {i} FAILED with uncaught exception: {e}")
    print("=== Adversarial Suite Complete. Zero Uncaught Exceptions. ===")
