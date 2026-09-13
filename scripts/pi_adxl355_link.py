#!/usr/bin/env python3
"""pi_adxl355_link.py
Week 2 #2 — analog (proof mass) to digital (20-bit I2C cells).
Rules: no numpy, no g-float, no stored negative, do not invent a shake.
Refuse: E_NO_BUS, E_NO_CHIP. 3.3 V only.

Pins (physical): 1=3V3, 3=SDA, 5=SCL, 6=GND. CS to 3V3.
ASEL GND -> 0x1D ; ASEL 3V3 -> 0x53.
"""

from __future__ import annotations

import os
import sys
import time

BUS = 1
ADDR_CANDIDATES = (0x1D, 0x53)
DEV_PATH = "/dev/i2c-%d" % BUS

REG_DEVID_AD = 0x00
REG_DEVID_MST = 0x01
REG_PARTID = 0x02
REG_XDATA3 = 0x08
REG_POWER_CTL = 0x2D
REG_RANGE = 0x2C

# ±2 g setting: 256000 LSB per g. Integer only.
LSB_PER_G = 256000
DEVID_AD_OK = 0xAD
PARTID_OK = 0xED

E_NO_BUS = "E_NO_BUS"
E_NO_CHIP = "E_NO_CHIP"


def refuse(code: str, detail: str) -> None:
    sys.stderr.write("%s %s\n" % (code, detail))
    sys.exit(1)


def open_bus():
    if not os.path.exists(DEV_PATH):
        refuse(E_NO_BUS, DEV_PATH + " missing — enable I2C and reboot")
    try:
        import smbus2
    except ImportError:
        refuse(E_NO_BUS, "smbus2 not installed — sudo apt install python3-smbus2")
    try:
        return smbus2.SMBus(BUS)
    except OSError as exc:
        refuse(E_NO_BUS, str(exc))


def peel20(b0: int, b1: int, b2: int) -> tuple[int, int]:
    """20-bit cell from 3 bytes. Invert-unit then add. No stored negative.
    Returns (magnitude, invert_flag). invert_flag 1 means the unit was inverted.
    """
    raw = ((b0 & 0xFF) << 12) | ((b1 & 0xFF) << 4) | ((b2 & 0xFF) >> 4)
    raw &= 0xFFFFF
    if raw & 0x80000:
        magnitude = (0x100000 - raw) & 0xFFFFF
        return magnitude, 1
    return raw, 0


def find_chip(bus) -> int:
    last = ""
    for addr in ADDR_CANDIDATES:
        try:
            devid = bus.read_byte_data(addr, REG_DEVID_AD)
            part = bus.read_byte_data(addr, REG_PARTID)
        except OSError as exc:
            last = str(exc)
            continue
        if devid == DEVID_AD_OK and part == PARTID_OK:
            return addr
        last = "DEVID=%s PARTID=%s at 0x%02X" % (hex(devid), hex(part), addr)
    refuse(E_NO_CHIP, "neither 0x1D nor 0x53 answered AD/ED — " + last)


def wake(bus, addr: int) -> None:
    # RANGE bits [1:0] = 01 -> ±2 g. Keep other bits clear.
    bus.write_byte_data(addr, REG_RANGE, 0x01)
    # POWER_CTL = 0 -> measurement mode (standby bit off).
    bus.write_byte_data(addr, REG_POWER_CTL, 0x00)
    time.sleep(0.05)


def read_xyz(bus, addr: int):
    block = bus.read_i2c_block_data(addr, REG_XDATA3, 9)
    x_mag, x_inv = peel20(block[0], block[1], block[2])
    y_mag, y_inv = peel20(block[3], block[4], block[5])
    z_mag, z_inv = peel20(block[6], block[7], block[8])
    return (x_mag, x_inv, y_mag, y_inv, z_mag, z_inv)


def to_milli_g(magnitude: int) -> int:
    return (magnitude * 1000) // LSB_PER_G


def main() -> int:
    bus = open_bus()
    addr = find_chip(bus)
    wake(bus, addr)
    sys.stdout.write("CHIP 0x%02X bus %d LSB_PER_G %d\n" % (addr, BUS, LSB_PER_G))
    sys.stdout.flush()
    try:
        while True:
            x_mag, x_inv, y_mag, y_inv, z_mag, z_inv = read_xyz(bus, addr)
            line = (
                "X %d mg inv %d  Y %d mg inv %d  Z %d mg inv %d  "
                "raw %d %d %d"
                % (
                    to_milli_g(x_mag),
                    x_inv,
                    to_milli_g(y_mag),
                    y_inv,
                    to_milli_g(z_mag),
                    z_inv,
                    x_mag,
                    y_mag,
                    z_mag,
                )
            )
            sys.stdout.write(line + "\n")
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        bus.write_byte_data(addr, REG_POWER_CTL, 0x01)
        return 0


if __name__ == "__main__":
    sys.exit(main())
