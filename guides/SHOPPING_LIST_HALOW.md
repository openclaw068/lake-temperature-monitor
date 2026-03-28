# Shopping List — Wi‑Fi HaLow (802.11ah) Lake Temp Monitor (US 902–928 MHz)

This is the **cheapest practical HaLow architecture** (Option 1).

## HaLow Link (core)
### Home side
1) **Heltec HT‑H7608 V2 HaLow Router/Gateway** (902–928 MHz US)
- Link: https://www.amazon.com/HT-H7608-802-11ah-Dual-Band-Transmission-902-928MHz/dp/B0F2HT6ZFX

### Dock side
2) **Heltec Wi‑Fi HaLow Dongle V2 (HT‑HD01)** (902–928 MHz US)
- Link: https://www.amazon.com/Heltec-Wireless-802-11ah-Extender-AP/dp/B0DXKW4V4J

## Antennas (recommended for ~1 mile)
3) **902–928 MHz directional Yagi antennas** (buy 2, one per side)
- Example (14 dBi): https://www.amazon.com/902-928-MHz-dbi-Yagi-antenna/dp/B01E2RXJA4

Notes:
- Keep coax as short as possible.
- Mount antennas higher = better link.

## Dock compute + sensing
4) **Raspberry Pi Zero 2 W** (dock compute)
- You’ll also need a microSD card and a 5V power regulator.

5) **DS18B20 waterproof temperature probes** (water + air)
- Qty: 2 (a 3-pack is fine)

6) **4.7 kΩ resistor** (1‑Wire pull‑up)

## Dock power + enclosure
7) Solar panel + charge controller + battery + weatherproof enclosure
- Exact sizing depends on whether you keep the dock Pi powered continuously.
- If you want “always-on HaLow + MQTT”, plan larger than the LoRa build.

Recommended starting point:
- 20W 12V solar panel
- 12V LiFePO4 battery (10Ah)
- 12V→5V buck converter (3A)
- IP67 enclosure + cable glands

---

## Optional (camera later)
- Camera module depends on whether you use a Pi camera or USB camera.
- HaLow can handle occasional snapshots; LoRa cannot.
