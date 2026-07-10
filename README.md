# Mine Safety Edge-AI System
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white) ![MATLAB](https://img.shields.io/badge/MATLAB-%23e05a00.svg?style=for-the-badge) ![Simulink](https://img.shields.io/badge/Simulink-%23e05a00.svg?style=for-the-badge)

## Overview
An edge safety system deploying deterministic ML fall-detection models directly on ESP32 microcontrollers with a memory footprint under 128KB. Features event-driven C++ firmware that prioritizes alert transmission packets over telemetry updates during latency-critical hazard events.

## System Architecture
```\n[Relational Database / Core API Architecture]\n```

## Features
- Real-time fall classification running on ESP32 microcontrollers (<128KB memory footprint).
- Event-driven firmware prioritizing safety alert packets over standard sensor telemetry during critical events.
- Multi-sensor data acquisition (accelerometer, gyroscope) processed on-chip.

## Tech Stack
- ESP32 microcontrollers (C++ PlatformIO / Arduino IDE)
- MATLAB & Simulink for data simulation and model verification
- Analog & digital sensors (accelerometers, gyroscopes, gas detectors)

## Getting Started
To configure and run the project locally, clone the repository and execute the setup instructions:

```bash
git clone https://github.com/Raghuram-sekar/Mine-Safety-Edge-AI.git
cd Mine-Safety-Edge-AI

# Execute local setup commands:
# Open project in Arduino IDE or PlatformIO
# Compile and upload to ESP32 board
```
