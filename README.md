# Lake Temperature Monitor (Wi‑Fi HaLow 802.11ah + Home Assistant)

This repo is the **Wi‑Fi HaLow (802.11ah)** version of the lake temperature monitor.

## Why HaLow
- **Sub‑GHz long range (US 902–928 MHz)**
- **IP-native link** (unlike LoRa packets)
- Enough bandwidth for sensor data *and* (optionally) occasional low-res snapshots

## The key design constraint
**ESPHome does not currently support Wi‑Fi HaLow.**

So instead of “ESPHome device → HA discovery”, this design uses:
- A HaLow link to extend your network
- A small Linux node at the dock that reads sensors and publishes to Home Assistant via **MQTT**

## Cheapest recommended architecture (picked for you)
You asked me to pick the cheapest of two approaches.

**Chosen:** **Option 1 (Heltec HaLow gear)** — cheapest practical path.

### Home side
- **Heltec HT‑H7608 V2** (HaLow router/gateway, OpenWrt-based)
- Directional antenna mounted high and aimed toward the dock (recommended for 1 mile)

### Dock side
- **Heltec HaLow Dongle V2 (HT‑HD01)** (HaLow client/bridge)
- **Raspberry Pi Zero 2 W** (or similar Linux SBC) to read DS18B20 sensors
- Solar + battery + enclosure

## Repository contents
- `guides/SHOPPING_LIST_HALOW.md` — HaLow shopping list with links (US 902–928)
- `guides/ARCHITECTURE_HALOW.md` — how the pieces connect
- `dock-node/` — scripts + config for the dock Linux node
- `home-assistant/` — HA MQTT config examples + dashboard card
- `legacy-lora-esphome/` — the previous LoRa+ESPHome guide and YAML (kept for reference)

## Quick start (once hardware arrives)
1) Bring up the HaLow link (home gateway + dock dongle)
2) Bring up MQTT on Home Assistant (Mosquitto add-on/integration)
3) On the dock Pi, run the publisher in `dock-node/` (systemd service included)
4) Confirm entities show in Home Assistant

---

If you want, I can also add an optional camera module plan (still over HaLow, not LoRa).
