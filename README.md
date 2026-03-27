# Lake Temperature Monitor (LoRa + ESPHome + Home Assistant)

This repo contains the **audited / corrected v2 build guide** for a solar-powered, off-grid lake temperature monitor:
- Dock node: Heltec WiFi LoRa 32 V3 (SX1262 @ 915MHz) + 2x DS18B20 (water + air) + solar + 18650
- Gateway node: Heltec V3 inside the house on Wi‑Fi, receives LoRa packets and exposes sensors to Home Assistant via ESPHome API

## What’s in here
- `lake temp monitor guide v2.pdf` — the original PDF artifact
- `lake-temp-monitor-guide-v2.txt` — extracted text version (easy to diff/search)

## Quick start
1. Read the guide (Section 3 shopping list + Sections 4–7 build + firmware).
2. When you’re ready to flash, install ESPHome (either via Home Assistant add-on or CLI).
3. Use the YAML in Section 7 of the guide for:
   - Address scanner (to capture DS18B20 addresses)
   - Dock node firmware (deep sleep + transmit)
   - Gateway firmware (Wi‑Fi + receive + publish template sensors)

## Notes
- The v2 guide fixes ESPHome YAML issues from v1 that would have caused compile failures (SX126x keys/fields, packet TX/RX API usage, and payload packing).
- Battery ADC pin varies by Heltec V3 hardware revision; verify against your board schematic.

## License
Unlicensed (private use). Add a license if you want this public.
