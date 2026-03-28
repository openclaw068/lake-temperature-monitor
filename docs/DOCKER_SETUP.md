# Home Assistant (Docker) + ESPHome (Docker) Setup

This project works well with **Home Assistant Container** on a Linux server.

## Why `network_mode: host`
ESPHome device discovery and Home Assistant integrations are much smoother on host networking (mDNS/SSDP/broadcast traffic).

## Prereqs
- Linux server (x86_64) with Docker + docker-compose plugin
- A user with permission to run docker

## Quick start
From the repo root:

```bash
mkdir -p ha_config esphome_config

docker compose up -d
```

Then:
- Home Assistant UI: `http://<server-ip>:8123`
- ESPHome UI: `http://<server-ip>:6052`

## ESPHome + flashing
You have two options:

### Option A (recommended): flash from your laptop/desktop
- Install ESPHome on your PC just for initial flashing.
- After the gateway is on Wi‑Fi, you can manage it from the ESPHome container via OTA.

### Option B: flash from the Linux server via USB passthrough
1. Plug the Heltec board into the server via USB.
2. Find the serial device:
   ```bash
   ls -l /dev/serial/by-id/
   ```
3. Edit `docker-compose.yml` and map that device under the `esphome:` service (preferred), e.g.:
   ```yaml
   devices:
     - /dev/serial/by-id/usb-...:/dev/ttyUSB0
   ```

If you can’t get stable permissions, you can (temporarily) use:
```yaml
privileged: true
```

## Using the YAML in this repo
Copy the YAML files from `./esphome/` into the ESPHome dashboard (UI) or into `./esphome_config/`.

Suggested mapping:
- `esphome/address-scanner.yaml` → `esphome_config/address-scanner.yaml`
- `esphome/dock-node.yaml` → `esphome_config/lake-dock-node.yaml`
- `esphome/gateway.yaml` (indoor) OR `esphome/gateway-solar-outdoor.yaml` → `esphome_config/lake-gateway.yaml`

## Notes
- If you already have Home Assistant running elsewhere, you can still run only the ESPHome container.
- If you use VLANs, ensure ESPHome devices can reach HA on TCP 6053.
