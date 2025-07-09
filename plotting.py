

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def plot_3d_trajectory(drone, interceptor):
        positions_drone = np.array(drone.history)
        positions_interceptor = np.array(interceptor.history)
        
        # Create a 3D plot
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot trajectory
        ax.plot(positions_drone[:, 0], positions_drone[:, 1], positions_drone[:, 2],
                 'b-', linewidth=2, label='Trajectory')
        
        ax.plot(positions_interceptor[:, 0], positions_interceptor[:, 1], positions_interceptor[:, 2],
                'r-', linewidth=2, label='Interceptor Trajectory')
        
        # Mark start and end positions
        ax.scatter(positions_drone[0, 0], positions_drone[0, 1], positions_drone[0, 2], 
                  color='green', s=100, label='Start', marker='o')
        ax.scatter(positions_drone[-1, 0], positions_drone[-1, 1], positions_drone[-1, 2], 
                  color='red', s=100, label='End', marker='x')
        
        ax.scatter(positions_interceptor[0, 0], positions_interceptor[0, 1], positions_interceptor[0, 2],
                    color='orange', s=100, label='Interceptor Start', marker='o')
        ax.scatter(positions_interceptor[-1, 0], positions_interceptor[-1, 1], positions_interceptor[-1, 2],
                    color='purple', s=100, label='Interceptor End', marker='x')
        
        # Add velocity vector at current position
        current_pos_drone = positions_drone[-1]
        ax.quiver(current_pos_drone[0], current_pos_drone[1], current_pos_drone[2],
                 drone.velocity[0], drone.velocity[1], drone.velocity[2],
                 color='red', arrow_length_ratio=0.1, label='Current Velocity')
        
        current_pos_interceptor = positions_interceptor[-1]
        ax.quiver(current_pos_interceptor[0], current_pos_interceptor[1], current_pos_interceptor[2],
                 interceptor.velocity[0], interceptor.velocity[1], interceptor.velocity[2],
                 color='blue', arrow_length_ratio=0.1, label='Interceptor Velocity')
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Z Position')
        ax.set_title('Drone 3D Trajectory')
        ax.legend()
        ax.grid(True)
        
        plt.show()
    


def plot_position_vs_time(drone, interceptor):
        """Plot position components vs time"""
    
        positions_drone = np.array(drone.history)
        positions_interceptor = np.array(interceptor.history)
        times_drone = np.array(drone.time_history)
        times_interceptor = np.array(interceptor.time_history)
        
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
        
        ax1.plot(times_drone, positions_drone[:, 0], 'r-', linewidth=2, label='X position')
        ax1.plot(times_interceptor, positions_interceptor[:, 0], 'r--', linewidth=2, label='Interceptor X position')
        ax1.set_ylabel('X Position')
        ax1.grid(True)
        ax1.legend()

        ax2.plot(times_drone, positions_drone[:, 1], 'g-', linewidth=2, label='Y position')
        ax2.plot(times_interceptor, positions_interceptor[:, 1], 'g--', linewidth=2, label='Interceptor Y position')
        ax2.set_ylabel('Y Position')
        ax2.grid(True)
        ax2.legend()

        ax3.plot(times_drone, positions_drone[:, 2], 'b-', linewidth=2, label='Z position')
        ax3.plot(times_interceptor, positions_interceptor[:, 2], 'b--', linewidth=2, label='Interceptor Z position')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Z Position')
        ax3.grid(True)
        ax3.legend()
        
        plt.suptitle('Drone Position Components vs Time')
        plt.tight_layout()
        plt.show()


        positions_drone = np.array(drone.history)
        positions_interceptor = np.array(interceptor.history)

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Set axis limits based on trajectory bounds
        ax.set_xlim(positions_drone[:, 0].min() - 1, positions_drone[:, 0].max() + 1)
        ax.set_ylim(positions_drone[:, 1].min() - 1, positions_drone[:, 1].max() + 1)
        ax.set_zlim(positions_drone[:, 2].min() - 1, positions_drone[:, 2].max() + 1)
        # Set limits for interceptor
        ax.set_xlim(positions_interceptor[:, 0].min() - 1, positions_interceptor[:, 0].max() + 1)
        ax.set_ylim(positions_interceptor[:, 1].min() - 1, positions_interceptor[:, 1].max() + 1)
        ax.set_zlim(positions_interceptor[:, 2].min() - 1, positions_interceptor[:, 2].max() + 1)

        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Z Position')
        ax.set_title('Animated Drone and Interceptor Movement')
        ax.view_init(elev=20, azim=-30)  # Set initial view angle
        ax.grid(True)
        # Plot interceptor trajectory
        # Initialize empty line for trajectory
        line, = ax.plot([], [], [], 'b-', linewidth=2, label='Trajectory')
        point, = ax.plot([], [], [], 'ro', markersize=8, label='Drone')
        
        def animate(frame):
            if frame < len(positions_drone):
                # Update trajectory up to current frame
                line.set_data(positions_drone[:frame+1, 0], positions_drone[:frame+1, 1])
                line.set_data(positions_interceptor[:frame+1, 0], positions_interceptor[:frame+1, 1])
                line.set_3d_properties(positions_interceptor[:frame+1, 2])
                line.set_3d_properties(positions_drone[:frame+1, 2])

                # Update current position
                point.set_data([positions_drone[frame, 0]], [positions_drone[frame, 1]])
                point.set_data([positions_interceptor[frame, 0]], [positions_interceptor[frame, 1]])
                point.set_3d_properties([positions_interceptor[frame, 2]])
                point.set_3d_properties([positions_drone[frame, 2]])

                ax.set_title(f'Animated Drone and interceptor Movement - Time: {drone.time_history[frame]:.2f}s')

            
            return line, point
        
        ax.legend()
        ani = FuncAnimation(fig, animate, frames=len(positions_drone), interval=interval, blit=False)
        plt.show()
        return ani
