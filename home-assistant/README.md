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

## Next step
We can add an HA MQTT sensor config (or MQTT Discovery) once we confirm your preferred entity names.
