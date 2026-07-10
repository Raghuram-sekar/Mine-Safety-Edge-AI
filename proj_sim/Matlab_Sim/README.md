MATLAB Simulation — Mine Safety Edge-AI System
Overview

This folder contains the system-level MATLAB simulation of a safety-critical mine monitoring system.
The simulation models the complete IoT pipeline:

Sensors → Edge AI (ESP) → LoRa Communication → Server Dashboard

The simulation is modular, time-driven, and designed to visually and logically demonstrate system behavior under normal, emergency, and failure conditions.

Simulation Objectives

Demonstrate edge-based decision making

Validate fail-safe system behavior

Model event-driven LoRa communication

Visualize multi-node monitoring at the server

Provide an exam-safe, professional system simulation

Note:
This simulation focuses on system behavior, not PHY-level modulation details.

Module Structure:
MATLAB_Simulation/
│
├── module1_sensor_animation.m
├── module2_esp_edge_emulator_failsafe.m
├── module3_lora_packet_simulation.m
├── module4_multinode_dashboard.m
└── README.md

MODULE 1 — Sensor Modeling & Animation
File: module1_sensor_animation.m
Purpose

Simulates real-world sensor behavior in a mining environment.

Sensors Modeled

Gas concentration (MQ-135 equivalent)

Acceleration magnitude (IMU)

Gyroscope magnitude (IMU)

Temperature (DHT11)

Humidity (DHT11)

Key Features

Time-driven simulation (1 Hz)

Noise-aware signals

Injected events:

Gas leakage

Worker fall

Environmental change

Output

Animated sensor plots

Ground-truth signals used by the ESP emulator

Why this matters

Provides realistic inputs to the edge system while remaining hardware-independent.

MODULE 2 — ESP Edge AI Emulator with Fail-Safe Logic
File
module2_esp_edge_emulator_failsafe.m

Purpose

Emulates the embedded ESP node, including:

Feature extraction

ML inference

Safety overrides

Failure handling

Operations Performed

Rolling-window feature extraction

Feature normalization

Pretrained linear ML inference

Rule-based fall detection

Fail-safe decision hierarchy

Fail-Safe Conditions Modeled

Power failure → ESP OFFLINE

Sensor failure → SENSOR FAULT

Fall detection → EMERGENCY override

Decision Priority
Power failure
→ Sensor failure
→ Fall detection
→ ML inference

Output

Color-coded ESP status animation

Deterministic state transitions

Why this matters

Demonstrates true edge intelligence with safety-critical guarantees.

MODULE 3 — Packet-Level LoRa Communication
File
module3_lora_packet_simulation.m

Purpose

Simulates event-driven LoRa uplink communication at the packet level.

Why Packet-Level?

MATLAB does not provide a dedicated LoRa PHY toolbox

System-level IoT evaluation focuses on:

Latency

Reliability

Event delivery

Communication Model

Uplink only (ESP → Gateway)

Transmissions occur only during emergencies or faults

No periodic data flooding

Channel Effects Modeled

Random transmission delay

Packet loss probability

Node offline behavior

Packet Contents
Node ID
Timestamp
Status (WARNING / EMERGENCY / OFFLINE)

Output

Packet sent / received / lost visualization

Gateway event log

Why this matters

Accurately reflects LPWAN behavior in real IoT systems.

MODULE 4 — Multi-Node Server Dashboard
File
module4_multinode_dashboard.m

Purpose

Implements a centralized monitoring dashboard for multiple ESP nodes.

Supported Features

Multi-node status tracking

Independent node failure handling

Offline detection using timeouts

Centralized event logging

Dashboard Panels

Per-node status indicators

Network health summary

Time-stamped event table

Scalability

Easily extendable to more nodes

Each node operates independently

Why this matters

Demonstrates real-world mine-scale deployment capability.

End-to-End System Flow: 
Module 1: Sensors
     ↓
Module 2: Edge AI + Fail-Safe
     ↓
Module 3: Event-Driven LoRa
     ↓
Module 4: Multi-Node Dashboard
Each module is:

Independently testable

Logically connected

Key Design Principles Demonstrated:

    Edge-first intelligence
    Event-driven communication
    Fail-safe priority over ML
    Deterministic embedded logic
    Scalable multi-node monitoring

How to Use This Simulation:

Run modules in order for best understanding
Each module can also be demonstrated independently
Recommended demo order:
Module 1 → Module 2 → Module 3 → Module 4

Future Extensions (Not Implemented)

LoRaWAN MAC modeling

Multi-gateway redundancy

Zone-based mine monitoring

Real hardware-in-loop testing



