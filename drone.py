import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import time
from threading import Thread



class Drone:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.time_reading = 0.0 # start time reading at 0.0
        self.history = [self.position.copy()] # to store the history of positions for plotting the trajectory
        self.time_history = [0.0]  # to store time history
        self.is_flying = False # initially not active
        
        # For continuous radar updates
        self.is_sending_radar_updates = False
        self.radar_update_thread = None
        self.radar = None
    
    def start_flying(self):
        self.is_flying = True
        print("[DRONE] Started flying mode")
    
    def stop_flying(self):
        self.is_flying = False
        print("[DRONE] Stopped flying mode")
    
    def update_position(self, dt, velocity):
        self.position += velocity * dt
        self.history.append(self.position.copy()) 
        self.time_history.append(self.time_reading)  
    
    
    
    def plot_3d_trajectory(self):
        """Plot the 3D trajectory of the drone"""
        if len(self.history) < 2:
            print("Not enough position data to plot")
            return
        
        # getting the positions from history
        # to plot the trajectory in 3D
        positions = np.array(self.history)
        
        # Create a 3D plot
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot trajectory
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', linewidth=2, label='Trajectory')
        
        # Mark start and end positions
        ax.scatter(positions[0, 0], positions[0, 1], positions[0, 2], 
                  color='green', s=100, label='Start', marker='o')
        ax.scatter(positions[-1, 0], positions[-1, 1], positions[-1, 2], 
                  color='red', s=100, label='End', marker='x')
        
        # Add velocity vector at current position
        current_pos = positions[-1]
        ax.quiver(current_pos[0], current_pos[1], current_pos[2],
                 self.velocity[0], self.velocity[1], self.velocity[2],
                 color='red', arrow_length_ratio=0.1, label='Current Velocity')
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Z Position')
        ax.set_title('Drone 3D Trajectory')
        ax.legend()
        ax.grid(True)
        
        plt.show()
    
    def plot_position_vs_time(self):
        """Plot position components vs time"""
        if len(self.history) < 2:
            print("Not enough position data to plot")
            return
        
        positions = np.array(self.history)
        times = np.array(self.time_history)
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
        
        ax1.plot(times, positions[:, 0], 'r-', linewidth=2, label='X position')
        ax1.set_ylabel('X Position')
        ax1.grid(True)
        ax1.legend()
        
        ax2.plot(times, positions[:, 1], 'g-', linewidth=2, label='Y position')
        ax2.set_ylabel('Y Position')
        ax2.grid(True)
        ax2.legend()
        
        ax3.plot(times, positions[:, 2], 'b-', linewidth=2, label='Z position')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Z Position')
        ax3.grid(True)
        ax3.legend()
        
        plt.suptitle('Drone Position Components vs Time')
        plt.tight_layout()
        plt.show()
    
    def animate_movement(self, interval=100):
        """Create an animated plot of the drone movement"""
        if len(self.history) < 2:
            print("Not enough position data to animate")
            return
        
        positions = np.array(self.history)
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Set axis limits based on trajectory bounds
        ax.set_xlim(positions[:, 0].min() - 1, positions[:, 0].max() + 1)
        ax.set_ylim(positions[:, 1].min() - 1, positions[:, 1].max() + 1)
        ax.set_zlim(positions[:, 2].min() - 1, positions[:, 2].max() + 1)
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Z Position')
        ax.set_title('Animated Drone Movement')
        
        # Initialize empty line for trajectory
        line, = ax.plot([], [], [], 'b-', linewidth=2, label='Trajectory')
        point, = ax.plot([], [], [], 'ro', markersize=8, label='Drone')
        
        def animate(frame):
            if frame < len(positions):
                # Update trajectory up to current frame
                line.set_data(positions[:frame+1, 0], positions[:frame+1, 1])
                line.set_3d_properties(positions[:frame+1, 2])
                
                # Update current position
                point.set_data([positions[frame, 0]], [positions[frame, 1]])
                point.set_3d_properties([positions[frame, 2]])
                
                ax.set_title(f'Animated Drone Movement - Time: {self.time_history[frame]:.2f}s')
            
            return line, point
        
        ax.legend()
        ani = FuncAnimation(fig, animate, frames=len(positions), interval=interval, blit=False)
        plt.show()
        return ani

    def send_position_to(self, radar):
        """Single call to send position data to radar"""
        if not self.is_flying:
            print("Drone is not flying. Cannot send position data.")
            return
        position_to_send = self.position.copy()
        time_to_send = self.time_reading
        radar.capture_position_variations(position_to_send, time_to_send)
    
    def start_continuous_radar_updates(self, radar, update_interval=0.1):
        self.radar = radar
        if not self.is_sending_radar_updates:
            self.is_sending_radar_updates = True
            self.radar_update_thread = Thread(target=self._continuous_radar_updates, args=(update_interval,))
            self.radar_update_thread.daemon = True
            self.radar_update_thread.start()
            print("[DRONE] Started continuous radar updates thread")
    
    def stop_continuous_radar_updates(self):
        """Stop sending continuous radar updates"""
        self.is_sending_radar_updates = False
        if self.radar_update_thread:
            self.radar_update_thread.join()
        print("[DRONE] Stopped continuous radar updates thread")
    
    def _continuous_radar_updates(self, update_interval):
        while self.is_sending_radar_updates:
            if self.is_flying and self.radar:
                # Send position data to radar
                position_to_send = self.position.copy()
                time_to_send = self.time_reading
                print(f"[RADAR THREAD] Sending position from drone: {position_to_send} at time {time_to_send:.2f}s")
                self.radar.capture_position_variations(position_to_send, time_to_send)
            
            time.sleep(update_interval)
