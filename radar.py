from drone import Drone
import numpy as np

# Create a simple radar simulator
class Radar:
    def __init__(self):
        self.position_history = []
        self.time_history = []
    
    def capture_position_variations(self, position, time_reading):
        self.position_history.append(position.copy())
        self.time_history.append(time_reading)
        print(f"[RADAR] Received drone position: {position} at time {time_reading:.2f}s")