# Architecture — Wi‑Fi HaLow (802.11ah)

## Goal
Replace LoRa point-to-point packets with a **Wi‑Fi HaLow (802.11ah) IP link** so the dock node behaves like a normal network client from Home Assistant’s perspective.

## Components
### Home side
- **Heltec HT‑H7608 V2** HaLow router/gateway
- Directional antenna aimed at dock
- Ethernet uplink into your home network

### Dock side
- **Heltec HaLow Dongle V2** (HaLow client)
- A small Linux node (recommended: **Pi Zero 2 W**)
- DS18B20 probes (water + air)
- Solar + battery + IP67 enclosure

## Data flow
1) Dock node reads sensors (DS18B20)
2) Dock publishes MQTT messages over HaLow IP link
3) Home Assistant subscribes and shows entities

## Why MQTT
Because ESPHome doesn’t support HaLow today, MQTT is the most compatible “bridge” protocol:
- trivial to integrate into Home Assistant
- works over any IP link
- easy to debug (`mosquitto_sub`, `tcpdump`)

## Security
- Your HaLow link stays inside your network.
- Remote access remains **Tailscale-only** (recommended).
