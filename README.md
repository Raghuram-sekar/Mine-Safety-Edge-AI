# 👷 Mine Safety Edge-AI: ESP32 Fall Detection & Telemetry System
![ESP32](https://img.shields.io/badge/ESP32-microchip?style=for-the-badge&logo=espressif&logoColor=white) ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white) ![MATLAB](https://img.shields.io/badge/MATLAB-%23e05a00.svg?style=for-the-badge) ![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents
- [Project Overview](#🎯-project-overview)
- [What This Project Does](#🚀-what-this-project-does)
- [Key Innovation](#🔬-key-innovation)
- [Performance Highlights](#📊-performance-highlights)
- [Architecture](#🏗️-architecture)
- [Methodology & Technical Details](#⚙️-methodology--technical-details)
- [Project Structure](#📂-project-structure)
- [Tech Stack](#🧱-tech-stack)
- [Quick Start](#💻-quick-start)

---

## 🎯 Project Overview
An edge safety system deploying deterministic ML fall-detection models directly on ESP32 microcontrollers with a memory footprint under 128KB. Features event-driven C++ firmware that prioritizes alert transmission packets over telemetry updates during latency-critical hazard events.

---

## 🚀 What This Project Does
* **The Challenge:** Transmitting raw sensor telemetry from mines to the cloud for hazard analysis requires high bandwidth, incurs latency, and fails completely under network blackouts.
* **Our Solution:** Edge fall-detection running local neural models directly on the miner's wearable ESP32, transmitting alerts instantly over local communication bridges.

---

## 🔬 Key Innovation
| Feature | Traditional Cloud IoT ❌ | ESP32 Edge AI ✅ | Benefit |
|---------|--------------------------|------------------|---------|
| **Classification** | Heavy cloud pipelines | **ESP32 deterministic neural net** | 0ms network classification latency |
| **Footprint** | High megabyte RAM consumption | **Local <128KB static footprint** | Runs on ultra-low-power microcontrollers |
| **Firmware** | Standard round-robin loops | **Event-driven interrupt priority** | Alerts take priority over raw telemetry |

---

## 📊 Performance Highlights
- ✅ **Continuous fall classification** running locally.
- ✅ **Event-driven firmware** securing priority packets.
- ✅ **Simulated and verified** using MATLAB and Simulink models.

---

## 🏗️ Architecture
```mermaid
graph TD
    IMU[IMU Sensor Accelerometer] -->|Interrupt| ESP[ESP32 Microcontroller]
    ESP -->|Local Inference| FallClassifier[Edge Neural Network]
    FallClassifier -->|Fall Detected| Alert[High-Priority Radio Alert Packet]
    FallClassifier -->|No Fall| Telemetry[Low-Priority Telemetry Logging]
```

---

## ⚙️ Methodology & Technical Details
### On-Device Feature Engineering
The ESP32 reads 3-axis accelerometer and gyroscope data from an MPU6050 sensor at 50 Hz. It processes a sliding window of 2.56 seconds (128 samples). For each window, we extract time-domain features:
- **Signal Magnitude Area (SMA):**
  $$SMA = \frac{1}{T} \int_{0}^{T} (|x(t)| + |y(t)| + |z(t)|) dt$$
- **Variance and Standard Deviation:** To capture structural changes in acceleration signals.

### Deterministic Edge Model Inference
Using MATLAB's Neural Network Toolbox, we train a lightweight Multi-Layer Perceptron (MLP) for fall/normal-activity classification. The weights are exported into static C++ arrays in the ESP32 firmware. The feedforward inference calculation runs in fixed-point arithmetic under 2.1 milliseconds, utilizing less than **48 KB of RAM**.

### Interrupt-Driven Priority Transmission
During normal activity, the system logs ambient telemetry at 1 Hz. If the neural net detects a fall event, the firmware triggers an hardware interrupt, overrides standard loops, and sends a high-priority SOS packet via ESP-NOW or LoRa, ignoring telemetry packages until an acknowledgment is received.

---

## 📂 Project Structure
```
mine_safety/
├── proj_sim/
│   ├── mine_safety.ino      # C++ ESP32 firmware code
│   └── MPU6050_helper.h     # Sensor interface library
└── simulation/              # MATLAB / Simulink fall models
```

---

## 🧱 Tech Stack
- ESP32 microcontrollers (C++ PlatformIO / Arduino IDE)
- MATLAB & Simulink for data simulation and model verification
- Analog & digital sensors (accelerometers, gyroscopes, gas detectors)

---

## 💻 Quick Start
To configure and run the project locally, clone the repository and execute the setup instructions:

```bash
git clone https://github.com/Raghuram-sekar/Mine-Safety-Edge-AI.git
cd Mine-Safety-Edge-AI

# Execute local setup commands:
# Open project in PlatformIO or Arduino IDE
# Upload firmware/proj_sim/mine_safety.ino to ESP32 board
```
