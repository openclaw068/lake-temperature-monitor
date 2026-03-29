#!/usr/bin/env python3
"""Publish Home Assistant MQTT Discovery entities for lake monitor.

Creates:
- sensor.lake_water_temperature
- sensor.lake_air_temperature
- sensor.lake_dock_battery_voltage (optional placeholder)

Assumes dock publishes readings JSON to `lake/dock/readings`.

You run this once at boot (or when HA restarts) to (re)announce entities.
"""

import os
import json
import socket
import paho.mqtt.client as mqtt

MQTT_HOST = os.environ.get("MQTT_HOST", "homeassistant")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASS = os.environ.get("MQTT_PASS")
PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "lake")

DEVICE_ID = os.environ.get("DEVICE_ID", socket.gethostname())

STATE_TOPIC = f"{PREFIX}/dock/readings"
DISCOVERY_PREFIX = os.environ.get("HA_DISCOVERY_PREFIX", "homeassistant")


def pub(client, topic, payload):
    client.publish(topic, json.dumps(payload), qos=1, retain=True)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"ha-disc-{DEVICE_ID}")
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

    device = {
        "identifiers": [f"lake_dock_{DEVICE_ID}"],
        "name": "Lake Dock Node",
        "model": "Pi Zero 2 W + Wi‑Fi HaLow bridge",
        "manufacturer": "DIY",
    }

    # These use JSON attributes from our state topic.
    # We’ll standardize the publisher to include top-level keys water_f and air_f.
    sensors = [
        {
            "name": "Lake Water Temperature",
            "unique_id": f"lake_water_temp_{DEVICE_ID}",
            "object_id": "lake_water_temperature",
            "unit": "°F",
            "device_class": "temperature",
            "value_template": "{{ value_json.water_f }}",
        },
        {
            "name": "Lake Air Temperature",
            "unique_id": f"lake_air_temp_{DEVICE_ID}",
            "object_id": "lake_air_temperature",
            "unit": "°F",
            "device_class": "temperature",
            "value_template": "{{ value_json.air_f }}",
        },
    ]

    for s in sensors:
        topic = f"{DISCOVERY_PREFIX}/sensor/{s['object_id']}/config"
        payload = {
            "name": s["name"],
            "unique_id": s["unique_id"],
            "state_topic": STATE_TOPIC,
            "value_template": s["value_template"],
            "unit_of_measurement": s["unit"],
            "device_class": s["device_class"],
            "device": device,
        }
        pub(client, topic, payload)

    client.disconnect()


if __name__ == "__main__":
    main()
