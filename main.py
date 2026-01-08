import drone
from interceptor import Interceptor
from radar import Radar
from drone import Drone
import numpy as np
import time
from plotting import plot_3d_trajectory, plot_position_vs_time
from plotting import animate


class Main:
    def __init__(self):
        self.drone = Drone([-12, -12, -13], [6, 1.5, 10])
        self.radar = Radar()
        self.interceptor = Interceptor([5, 1, 10], [0, 0, 0])
        self.drone.start_flying()
        self.interceptor.start_flying()
        self.drone.start_continuous_radar_updates(self.radar, update_interval=0.1)
        self.radar.start_sending_updates_to_interceptor(
            self.interceptor, update_interval=0.1
        )

        # Simulation
        dt = 0.1
        for i in range(100):
            random_velocity_change = np.random.normal(0, 2.0, size=3)
            random_direction_change = np.random.uniform(-5, 5, size=3)

            # Occasionally make dramatic direction changes
            if np.random.random() < 0.2:  # 20% chance of dramatic change
                self.drone.velocity = np.random.uniform(-15, 15, size=3)
            else:
                self.drone.velocity += random_velocity_change + random_direction_change

            if np.random.random() < 0.1:  # 10% chance of acceleration burst
                acceleration = np.random.uniform(-10, 10, size=3)
                self.drone.velocity += acceleration

            # Limit maximum speed, for testing now
            max_speed = 40
            speed = np.linalg.norm(self.drone.velocity)
            if speed > max_speed:
                self.drone.velocity = (self.drone.velocity / speed) * max_speed

            self.drone.update_position(dt, self.drone.velocity)
            self.drone.time_reading += dt
            # Simulate real-time updates,
            # consistent timing, give time to threads to update foreward
            time.sleep(0.1)

            if i % 10 == 0:
                print(
                    f"[MAIN] Drone position: {self.drone.position}, velocity: {self.drone.velocity}"
                )

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
        # animate
        animate(self.drone, self.interceptor)


if __name__ == "__main__":
    main = Main()
    print("[MAIN] Simulation completed.")
