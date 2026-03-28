# Dock Node (HaLow) — Pi Zero 2 W

This folder contains a minimal MQTT publisher for the dock node.

## Wiring (DS18B20)
You’ll wire DS18B20 probes to the Pi’s 1‑Wire GPIO and read them via Linux `w1_therm`.

## Install
On the dock Pi:

```bash
sudo apt update
sudo apt install -y python3 python3-pip

sudo pip3 install paho-mqtt

sudo mkdir -p /opt/lake-temp
sudo cp lake_temp_publisher.py /opt/lake-temp/

# Enable 1-wire (requires reboot)
# Add to /boot/config.txt (or /boot/firmware/config.txt depending on OS):
# dtoverlay=w1-gpio

sudo reboot
```

## Run once (test)
```bash
MQTT_HOST=<your-ha-ip> python3 /opt/lake-temp/lake_temp_publisher.py
```

## Run as service
```bash
sudo cp lake-temp-publisher.service /etc/systemd/system/
# edit User= and MQTT_HOST= inside the service file
sudo systemctl daemon-reload
sudo systemctl enable --now lake-temp-publisher
sudo systemctl status lake-temp-publisher
```
