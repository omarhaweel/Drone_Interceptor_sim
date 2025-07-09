# Drone Interceptor Simulation

**Purpose:**  
A 3D simulation of an interceptor drone pursuing and attempting to intercept a moving target (aggressor) drone using evasion and pursuit dynamics.

---

## Description

This simulation is built for educational purposes and is not optimized for production use. It aims to demonstrate fundamental principles of:

Pursuit-evasion dynamics
3D radar tracking
Reinforcement learning (future)
Multi-threaded simulations (future)
The interceptor will eventually be trained using reinforcement learning with a reward-penalty system to improve its interception strategy in real-time simulations.

## 🚀 Overview

This project simulates a dynamic interaction between two drones in 3D space:

- **Aggressor Drone:** A target drone that enters the surveillance zone with a given velocity.
- **3D Radar System:** Models the surveillance space using X, Y, and Z coordinates, tracking drone movement over time.
- **Interceptor Drone:** A faster, more agile drone designed to pursue and intercept the aggressor.

The simulation currently uses basic physics and visualization. Future iterations will involve Reinforcement Learning and multithreading to enhance performance and learning capabilities.

---

## 📦 Requirements

- Python 3.8+
- `numpy`
- `matplotlib`

Install dependencies:

pip install numpy matplotlib

## RUN 
python3 main.py

