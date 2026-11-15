# Talking Plant 🌱

A pixel-faced plant companion for Raspberry Pi, plus a browser-based simulator.

## Try it without hardware
Open `web/index.html` in a browser. Choose a plant, adjust soil moisture, light and temperature, and watch the animated pixel face respond. The demo uses illustrative ranges, not scientifically validated watering thresholds.

## Raspberry Pi kiosk
Requires Raspberry Pi OS with desktop, Python 3 and an HDMI display. Install:

```bash
sudo apt update
sudo apt install -y python3-pygame
git clone https://github.com/sirioitalianfactory/talking-plant.git
cd talking-plant
python3 -m pi.main --mock
```

`--mock` runs a live simulator; no sensors needed. Press Esc to exit, left/right to change plants. Real sensor integration is planned and intentionally not represented as working.

## Structure
- `web/index.html`: responsive browser demo with interactive sensor simulation
- `pi/main.py`: Pygame fullscreen-capable pixel-face kiosk
- `pi/health.py`: shared Python rules and sample plant profiles
- `tests/test_health.py`: Python unit tests
- `.github/workflows/ci.yml`: test pipeline

## Sensor hardware plan
- Capacitive soil probe **with ADC** (e.g. ADS1115), since Raspberry Pi GPIO has no analog input.
- BH1750 I2C ambient light sensor, measured in lux.
- BME280 I2C ambient temperature sensor.

Calibrate each soil probe for dry and wet conditions. Soil percentage is a calibrated relative value, not universal volumetric water content. Light requirements are often expressed in daily light integral, which cannot be inferred from a single lux reading. The sample target ranges are **illustrative only** and must be adjusted for species, environment, and calibration.

## Deployment
The browser demo is static. It can be hosted on GitHub Pages (if enabled for the repository) or any static host; deploy the `web/` directory. A workflow is provided to deploy automatically to GitHub Pages once Pages is configured with GitHub Actions as its source.

## Roadmap
Sensor adapters, local SQLite profiles and history, calibration UI, offline kiosk, multi-plant support, alerts, and a proper species-care dataset.
