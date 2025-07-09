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
        self.intercept_speed = 30.0  # Interceptor moves much faster than drone to catch up

    def start_flying(self):
        self.is_flying = True
        print("[INTERCEPTOR] Started flying mode")
    
    def stop_flying(self):
        self.is_flying = False
        print("[INTERCEPTOR] Stopped flying mode")
    
    def initiate(self):
        if not self.is_flying:
            self.start_flying()
            print("[INTERCEPTOR] Interceptor initiated and ready to intercept")

    def update_position_from_radar(self, target_position, target_time):
        """Receive target position from radar and calculate intercept course"""
        if not self.is_flying:
            self.initiate()
            
        self.target_position = np.array(target_position, dtype=float)
        
        # Calculate time difference since last update
        dt = target_time - self.time_reading if self.time_reading > 0 else 0.1

        # Calculate direction vector towards target, by differentiating the target position and current position
        direction = self.target_position - self.position
        # Calculate distance to target
        distance = np.linalg.norm(direction)
        
        if distance > 0.0001:
            direction_normalized = direction / distance
            movement = direction_normalized * self.intercept_speed * dt
            self.position += movement
            self.velocity = direction_normalized * self.intercept_speed
        
        self.time_reading = target_time
        self.history.append(self.position.copy())
        self.time_history.append(self.time_reading)

        # Print occasionally
        if int(target_time * 10) % 5 == 0:
            print(f"[INTERCEPTOR] Moving to intercept target at: {self.target_position}, current pos: {self.position} at time {target_time:.2f}s")

    


