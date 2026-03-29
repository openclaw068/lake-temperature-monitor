# Home Assistant Integration (MQTT)

This HaLow version uses MQTT.

## Broker
Use one:
- Home Assistant **Mosquitto broker** add-on, or
- any MQTT broker reachable from HA

## Topic
Default topic prefix is `lake`.

The dock node publishes JSON to:
- `lake/dock/readings`

## MQTT Discovery (recommended)
This repo includes a helper that publishes Home Assistant MQTT Discovery configs so sensors appear automatically.

Dock side:
- `dock-node/mqtt/ha_discovery.py`

Run it once after the dock node can reach the MQTT broker.

## Camera ingest
If you run go2rtc (recommended), use `home-assistant/docker-compose.go2rtc.yml` + `home-assistant/go2rtc/go2rtc.yaml`.
Then add the stream in Home Assistant.
