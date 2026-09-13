# Pi 5 GPIO attachments — not the clock

SVCT 2026-09-12T22:30:00-04:00
Parent: pi5-gpio-time-rtc (Leaf 1 OPEN) + edge-delegate-shepherd-pi5
Source: Gmail 196592c54cef81ac (2025-04-21)

## Value

Inexpensive GPIO attachments from the 2025 extras table (T-Cobbler, breakout, DHT11, HiLetgo voltage, jumpers) still plug in. They are wiring.

They are not good enough *now* for this Pi because:

1. That mail named PiGPIO. Pi 5 GPIO is on RP1. pigpio / original RPi.GPIO / WiringPi do not run.
2. Pi 5 job is gather/sort (shepherd), not become the device. Precision GPIO belongs on Pico 2 PIO.
3. Two clocks fight. Onboard RTC wants J5 ML-2020. Do not buy DS3231. Clock still OPEN.

Ribbon and DHT22 stay for sensors *after* the stamp.
