# Mine Safety Edge-AI System

An edge safety system deploying deterministic ML fall-detection models directly on ESP32 microcontrollers with a memory footprint under 128KB. Features event-driven C++ firmware that prioritizes alert transmission packets over telemetry updates during latency-critical hazard events.

## Features
- Real-time fall classification running on ESP32 microcontrollers (<128KB memory footprint).
- Event-driven firmware prioritizing safety alert packets over standard sensor telemetry during critical events.
- Multi-sensor data acquisition (accelerometer, gyroscope) processed on-chip.

## Tech Stack
- ESP32
- C++
- Edge ML
- Sensors
- MATLAB
- Simulink

## Getting Started
To configure and run the project locally, clone the repository and execute the setup instructions:

```bash
git clone https://github.com/Raghuram-sekar/Mine-Safety-Edge-AI.git
cd Mine-Safety-Edge-AI

# Execute local setup commands:
# Open project in Arduino IDE or PlatformIO
# Compile and upload to ESP32 board
```
