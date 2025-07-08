# Drone_Interceptor_sim
A simulation of a drone and interceptor-drone in 3D space

# REQUIREMENTS
- Python 3.8+
- numpy
- matplotlib

# DESCRIPTION
This project is intened for learning purposes and is not optimized for performance.
Gradually will be improved by an interceptor drone that will try to intercept the target drone
using Reinforcement Learning to learn the best strategy to intercept a non-stationary target.

Multithreading will be implemented later to allow for faster computation with Reward-penalty approach
This will allow the interceptor to learn from multiple simulations at once.

# DEVELOPMENT PHASES
PHASE 1: DRONE SIMULATION implemented, visualized by matplotlib, X,Y,Z axes.
PHASE 2: ----- the Interceptor not implemented
PHASE 3: ----- Reinforcement Learning not implemented
PHASE 4: ----- Multithreading not implemented
PHASE 5: parameter optimization and performance improvements
PHASE 6: Get real-time data in format velocity on x,y,z every 0.1 seconds (Radar-like data) instead of random data
this can be achieved by by sectioning the 3D space into a 3D grid and fixing the 0,0,0 point as the center of the grid
in a real airspace

# RUN
python3 drone.py