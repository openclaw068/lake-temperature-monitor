#!/usr/bin/env python3
"""Lake temp dock node publisher (HaLow IP link)

Reads DS18B20(s) via Linux w1_therm and publishes to MQTT.

Assumptions:
- DS18B20(s) are wired and exposed under /sys/bus/w1/devices/28-*/w1_slave
- MQTT broker reachable (Home Assistant Mosquitto addon or separate broker)

This is intentionally minimal and dependency-light.
"""

import os
import glob
import time
import json
import socket
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

MQTT_HOST = os.environ.get("MQTT_HOST", "homeassistant.local")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASS = os.environ.get("MQTT_PASS")
MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "lake")
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "300"))

# Optional: map sensor IDs to friendly roles.
# Example: export WATER_SENSOR_ID=28-00000abc1234
WATER_SENSOR_ID = os.environ.get("WATER_SENSOR_ID")
AIR_SENSOR_ID = os.environ.get("AIR_SENSOR_ID")


def read_ds18b20(device_id: str) -> float:
    path = f"/sys/bus/w1/devices/{device_id}/w1_slave"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    if not lines or "YES" not in lines[0]:
        raise RuntimeError(f"Bad CRC/read for {device_id}")
    # second line contains t=xxxxx in millideg C
    parts = lines[1].split("t=")
    if len(parts) != 2:
        raise RuntimeError(f"Malformed w1_slave for {device_id}")
    mc = int(parts[1])
    return mc / 1000.0


def discover_sensors() -> list[str]:
    devs = glob.glob("/sys/bus/w1/devices/28-*/w1_slave")
    return [os.path.basename(os.path.dirname(p)) for p in devs]


def classify(sensor_ids: list[str]) -> dict:
    out = {}
    for sid in sensor_ids:
        if WATER_SENSOR_ID and sid == WATER_SENSOR_ID:
            out["water"] = sid
        elif AIR_SENSOR_ID and sid == AIR_SENSOR_ID:
            out["air"] = sid
        else:
            out.setdefault("other", []).append(sid)
    return out


def publish(client: mqtt.Client, topic: str, payload: dict):
    client.publish(topic, json.dumps(payload), qos=1, retain=False)


def main():
    hostname = socket.gethostname()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"lake-dock-{hostname}")
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    while True:
        sensor_ids = discover_sensors()
        roles = classify(sensor_ids)

        ts = datetime.now(timezone.utc).isoformat()

        readings = {}
        for sid in sensor_ids:
            try:
                c = read_ds18b20(sid)
                f = (c * 9.0 / 5.0) + 32.0
                readings[sid] = {"c": round(c, 2), "f": round(f, 2)}
            except Exception as e:
                readings[sid] = {"error": str(e)}

        payload = {
            "ts": ts,
            "host": hostname,
            "roles": roles,
            "readings": readings,
        }

        publish(client, f"{MQTT_TOPIC_PREFIX}/dock/readings", payload)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
