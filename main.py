from radar import Radar 
from drone import Drone  
import numpy as np
import time


class Main:
    
    radar = Radar()
    drone = Drone([0, 0, 0], [1, 0.5, 0.2])
    
    # Start flying and continuous radar updates
    drone.start_flying()
    drone.start_continuous_radar_updates(radar, update_interval=0.5)
    
    # Simulation of drone movement
    dt = 0.1
    for i in range(500):
        drone.update_position(dt, drone.velocity)
        drone.velocity += np.random.normal(0, 0.1, size=3)
        drone.time_reading += dt
        time.sleep(0.1)  # Simulate real-time
        
        if i % 10 == 0:
            print(f"[MAIN] Drone position: {drone.position}")
    
    # Stop updates
    drone.stop_continuous_radar_updates()
    # Stop flying
    drone.stop_flying()
    
    print(f"[RADAR] Total positions captured: {len(radar.position_history)}")
    
    # Visualization
    drone.plot_3d_trajectory()
    drone.plot_position_vs_time()
    drone.animate_movement(interval=200)  # Animation with 200ms between frames

if __name__ == "__main__":
    main = Main()
    print("[MAIN] Simulation completed.")



