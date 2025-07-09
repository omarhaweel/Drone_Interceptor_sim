import drone
from interceptor import Interceptor
from radar import Radar 
from drone import Drone  
import numpy as np
import time
from plotting import plot_3d_trajectory, plot_position_vs_time


class Main:
    def __init__(self):
        self.drone = Drone([-4, 3, 13], [12, 3, 20])
        self.radar = Radar()
        self.interceptor = Interceptor([50, 34, 4], [2, 2, 3])

        # Start flying and continuous radar updates
        self.drone.start_flying()
        self.interceptor.start_flying()
        self.drone.start_continuous_radar_updates(self.radar, update_interval=0.001)
        self.radar.start_sending_updates_to_interceptor(self.interceptor, update_interval=0.001)
        
        # Simulation of drone movement
        dt = 0.1
        for i in range(100):
            self.drone.update_position(dt, self.drone.velocity)
            self.drone.velocity += np.random.normal(-0.1, 0.1, size=3)
            self.drone.time_reading += dt
            time.sleep(0.1)  # Simulate real-time
            
            if i % 10 == 0:
                print(f"[MAIN] Drone position: {self.drone.position}")
            
        # do not stop drone uodating the radar
        self.drone.stop_flying()
        self.radar.stop_sending_updates()
        self.interceptor.stop_flying()
        
        print(f"last position DRONE: {self.drone.position}")
        print(f"last time reading DRONE: {self.drone.time_reading}")
        print(f"last position INTERCEPTOR: {self.interceptor.position}")
        print(f"last time reading INTERCEPTOR: {self.interceptor.time_reading}")
        print(f"[RADAR] Total positions captured: {len(self.radar.position_history)}")

        # Plotting 3D trajectory
        plot_3d_trajectory(self.drone, self.interceptor)
        # Plotting position vs time
        plot_position_vs_time(self.drone, self.interceptor)
      
  

if __name__ == "__main__":
    main = Main()
    print("[MAIN] Simulation completed.")



