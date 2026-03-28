# Lake Temperature Monitor (LoRa 915MHz + ESPHome + Home Assistant)

Solar-powered dock node measures **lake water temp + air temp** and transmits readings via **LoRa (SX1262 @ 915MHz)** to a **home gateway** that forwards the values into **Home Assistant** (via ESPHome native API).

This repo includes:
- The **audited/corrected v2 build guide** (PDF + text)
- Standalone ESPHome YAML files under `./esphome/`

## Hardware (high level)
- **2× Heltec WiFi LoRa 32 V3** (US 902–928MHz version, SX1262)
- **2× DS18B20 waterproof probes** (one water, one air)
- Dock node power: **6V solar + 1× 18650**

## Files
- `lake temp monitor guide v2.pdf` — full build guide (shopping list, wiring, deployment)
- `lake-temp-monitor-guide-v2.txt` — extracted text copy
- `esphome/address-scanner.yaml` — finds DS18B20 addresses
- `esphome/dock-node.yaml` — deep-sleeping transmitter (NO Wi‑Fi)
- `esphome/gateway.yaml` — always-on receiver + Home Assistant sensors (indoor/USB power)
- `esphome/gateway-solar-outdoor.yaml` — always-on receiver + Home Assistant sensors (outdoor/solar box)

## Recommended software approach (Docker on a Linux server)
This repo now assumes you’re running:
- **Home Assistant Container** on your Linux server
- **ESPHome Container** alongside it

Use the included `docker-compose.yml` and see:
- `docs/DOCKER_SETUP.md`

## Setup steps (ESPHome + flashing)
### Step 0 — Start Home Assistant + ESPHome (Docker)
From the repo root on your Linux server:

```bash
mkdir -p ha_config esphome_config

docker compose up -d
```

Then:
- Home Assistant: `http://<server-ip>:8123`
- ESPHome: `http://<server-ip>:6052`

For details (USB flashing vs flashing from a laptop), see `docs/DOCKER_SETUP.md`.

### Step 1 — Find your DS18B20 probe addresses
1. In ESPHome, create a new device using `esphome/address-scanner.yaml`.
2. Flash it to the *dock node* Heltec V3 over USB.
3. Open logs and record both DS18B20 addresses (label one **WATER**, one **AIR**).

### Step 2 — Configure and flash the dock node
1. Open `esphome/dock-node.yaml`
2. Replace the placeholder DS18B20 addresses with your real ones.
3. Flash to the dock node over USB.

Notes:
- The dock node intentionally has **no `wifi:` block**.
- It wakes up, sends one LoRa packet, then deep-sleeps for ~5 minutes.

### Step 3 — Configure and flash the gateway
Pick one gateway config:
- **Indoor/USB-powered gateway:** `esphome/gateway.yaml`
- **Outdoor/solar gateway:** `esphome/gateway-solar-outdoor.yaml`

Then:
1. Set your Wi‑Fi SSID/password.
2. In ESPHome, generate an API encryption key + OTA password (the UI will prompt you), and put them in the YAML.
3. Flash to the gateway over USB.
4. After it joins Wi‑Fi, Home Assistant should discover it as an ESPHome device.

### Step 1 — Find your DS18B20 probe addresses
1. In ESPHome, create a new device using `esphome/address-scanner.yaml`.
2. Flash it to the *dock node* Heltec V3 over USB.
3. Open logs and record both DS18B20 addresses (label one **WATER**, one **AIR**).

### Step 2 — Configure and flash the dock node
1. Open `esphome/dock-node.yaml`
2. Replace the placeholder DS18B20 addresses with your real ones.
3. Flash to the dock node over USB.

Notes:
- The dock node intentionally has **no `wifi:` block**.
- It wakes up, sends one LoRa packet, then deep-sleeps for ~5 minutes.

### Step 3 — Configure and flash the home gateway
Pick one gateway config:
- **Indoor/USB-powered gateway:** `esphome/gateway.yaml`
- **Outdoor/solar gateway:** `esphome/gateway-solar-outdoor.yaml`

Then:
1. Set your Wi‑Fi SSID/password (default SSID in solar version is `IoT`).
2. In ESPHome, generate an API encryption key + OTA password (the UI will prompt you), and put them in the YAML.
3. Flash to the gateway over USB.
4. After it joins Wi‑Fi, Home Assistant should discover it as an ESPHome device.

### Step 4 — Home Assistant entities
Once the gateway is added to HA, you should see:
- `sensor.lake_water_temperature`
- `sensor.lake_air_temperature`
- `sensor.dock_node_battery`

## Troubleshooting quick hits
- No packets received: verify LoRa settings match exactly on both nodes (frequency/bandwidth/SF/coding rate) and TCXO settings are present.
- DS18B20 reads -127°C / 85°C: wiring/pull-up resistor issue.
- Battery ADC pin varies by Heltec V3 revision: `GPIO37` might need to be changed (try `GPIO1`).

## Band / region note
This project is **US 915MHz (902–928MHz)**. Do not buy the EU 868MHz hardware.
