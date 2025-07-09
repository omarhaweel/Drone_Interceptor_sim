from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def plot_3d_trajectory(drone, interceptor):
        positions_drone = np.array(drone.history)
        positions_interceptor = np.array(interceptor.history)
        

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


def animate(drone, interceptor, interval=100):

    positions_drone = np.array(drone.history)
    positions_interceptor = np.array(interceptor.history)

    times_drone = np.array(drone.time_history)
    times_interceptor = np.array(interceptor.time_history)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Cmbined bounds for both trajectories
    all_x = np.concatenate([positions_drone[:, 0], positions_interceptor[:, 0]])
    all_y = np.concatenate([positions_drone[:, 1], positions_interceptor[:, 1]])
    all_z = np.concatenate([positions_drone[:, 2], positions_interceptor[:, 2]])

    # Set limits based on combined bounds + 1 for all axes as padding
    ax.set_xlim(all_x.min() - 1, all_x.max() + 1)
    ax.set_ylim(all_y.min() - 1, all_y.max() + 1)
    ax.set_zlim(all_z.min() - 1, all_z.max() + 1)


    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')

    ax.set_title('Animated Drone and Interceptor Movement')
    ax.view_init(elev=20, azim=-30)
    ax.grid(True)

    # Initialize empty lines for trajectories
    line_drone, = ax.plot([], [], [], 'b-', linewidth=3, label='Drone Trajectory')
    line_interceptor, = ax.plot([], [], [], 'r-', linewidth=1, label='Interceptor Trajectory')
    
    # Initialize points for current positions
    point_drone, = ax.plot([], [], [], 'bo', markersize=10, label='Drone Position')
    point_interceptor, = ax.plot([], [], [], 'ro', markersize=6, label='Interceptor Position')

    ax.legend()

    def animate_frame(frame):

        if frame < len(positions_drone):
            line_drone.set_data(positions_drone[:frame+1, 0], positions_drone[:frame+1, 1])
            line_drone.set_3d_properties(positions_drone[:frame+1, 2])
            point_drone.set_data([positions_drone[frame, 0]], [positions_drone[frame, 1]])
            point_drone.set_3d_properties([positions_drone[frame, 2]])
            current_time = times_drone[frame] if frame < len(times_drone) else times_drone[-1]
        else:
            # Keep last position visible
            point_drone.set_data([positions_drone[-1, 0]], [positions_drone[-1, 1]])
            point_drone.set_3d_properties([positions_drone[-1, 2]])
            current_time = times_drone[-1]

        # Update interceptor trajectory and position
        if frame < len(positions_interceptor):
            line_interceptor.set_data(positions_interceptor[:frame+1, 0], positions_interceptor[:frame+1, 1])
            line_interceptor.set_3d_properties(positions_interceptor[:frame+1, 2])
            point_interceptor.set_data([positions_interceptor[frame, 0]], [positions_interceptor[frame, 1]])
            point_interceptor.set_3d_properties([positions_interceptor[frame, 2]])
        else:
            # Keep last position visible
            point_interceptor.set_data([positions_interceptor[-1, 0]], [positions_interceptor[-1, 1]])
            point_interceptor.set_3d_properties([positions_interceptor[-1, 2]])

        ax.set_title(f'Animated Drone and Interceptor Movement - Time: {current_time:.2f}s')
        return line_drone, point_drone, line_interceptor, point_interceptor

    # Use the maximum number of frames from both objects
    max_frames = max(len(positions_drone), len(positions_interceptor))
    animation = FuncAnimation(fig, animate_frame, frames=max_frames, interval=interval, blit=False, repeat=True)
    
    plt.show()
    return animation
