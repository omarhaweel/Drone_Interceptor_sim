import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import time
import threading
from drone import Drone

class Interceptor():
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.time_reading = 0.0 
        self.history = [self.position.copy()] 
        self.time_history = [0.0]  
        self.is_flying = False

        # Target tracking
        self.target_position = np.array(position, dtype=float)
        self.target_velocity = np.array(velocity, dtype=float)
        self.target_time = 0.0
        

        self.is_moving = False
        self.movement_thread = None
        self.intercept_speed = 2.0  # Interceptor moves faster than drone

    def start_flying(self):
        self.is_flying = True

        print("[INTERCEPTOR] Started flying mode")
    
    def stop_flying(self):
        self.is_flying = False
        print("[INTERCEPTOR] Stopped flying mode")
    

    def update_position_from_radar(self, target_position, target_time):
        """Receive target position from radar and calculate intercept course"""
        self.position = np.array(target_position, dtype=float)
        self.time_reading = target_time
        self.history.append(self.position.copy())
        self.time_history.append(self.time_reading)
        print(f"[INTERCEPTOR] Received target at: {self.position} at time {target_time:.2f}s")

    


