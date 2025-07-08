from radar import Radar 
from drone import Drone  
import numpy as np
import time


def main():
    drone_start_position = np.array([0, 0, 0], dtype=float)  # Starting position of the drone
    drone_start_velocity = np.array([0, 0, 0], dtype=float)  # Starting velocity of the drone in x, y, z axes
    drone = Drone(drone_start_position, drone_start_velocity)
    radar = Radar() 
    dt = 0.1

    print("Starting drone simulation...")
    iterations = 50
    for i in range(iterations):  # Reduced iterations for better visualization
        if not drone.is_flying:
            drone.is_flying = True
            print("Drone is now flying.")
        drone.update_position(dt, drone.velocity)
        drone.velocity += np.random.normal(-0.1, 1, size=3) # velocity can be captured from radar or other sensors to get real-time updates
        drone.time_reading += dt # increment time reading for each iteration and position update
        drone.send_position_to(radar)
        # sleep
        time.sleep(dt)

        # Print status every 10 iterations
        if i%10 == 0:
            print(f"Time: {drone.time_reading:.2f}s, Position: {drone.position}, Velocity: {drone.velocity}")
    
    # Final position after all iterations
    print("Drone final position after iterations:", drone.position)
    print("Generating 3d graph . . .")
    
    # Show the visualizations
    drone.plot_3d_trajectory()
    drone.plot_position_vs_time()
    drone.animate_movement(interval=200)  # Animation with 200ms between frames

if __name__ == "__main__":
    main()