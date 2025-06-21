# OBD2 Car Dashboard

A multiplatform (Windows, Linux, Android, macOS) Python-based OBD2 Car Dashboard app.  
Connects to Bluetooth OBD2 devices to display real-time speed, RPM, temperature, and more, with a car-friendly UI.  
Includes a built-in OBD2 device emulator for easy testing.

## Features

- Real-time OBD2 data: speed, RPM, coolant temp, engine load, fuel level
- Bluetooth (classic & BLE) device scanning and connection
- Built-in emulator for development/testing without hardware
- Car-friendly, touch-optimized UI (Kivy/KivyMD)
- Cross-platform: Windows, Linux, macOS, Android (via buildozer)
- Automated releases (see below)

## Quick Start

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```
   python main.py
   ```

3. **To test without a real OBD2 device:**  
   The built-in emulator will start automatically if no device is connected.

## Building for Android

- Install [buildozer](https://github.com/kivy/buildozer)
- Run:
  ```
  buildozer init
  buildozer -v android debug
  ```

## Automated Releases

This project uses GitHub Actions to build and publish releases automatically.  
See `.github/workflows/release.yml` for details.

## License

MIT
