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
        self.time_reading = 0.0
        self.history = [self.position.copy()]
        self.time_history = [0.0]
        self.is_flying = False

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

    def start_continuous_radar_updates(self, radar, update_interval=0.1):
        self.radar = radar
        if not self.is_sending_radar_updates:
            self.is_sending_radar_updates = True

            self.radar_update_thread = Thread(
                target=self._continuous_radar_updates, args=(update_interval,)
            )
            self.radar_update_thread.daemon = True

            self.radar_update_thread.start()
            print("[DRONE] Started continuous radar updates thread")

    def stop_continuous_radar_updates(self):
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
                print(
                    f"Sending position and time from drone to Radar: {position_to_send} at time {time_to_send:.2f}s"
                )
                self.radar.capture_position_variations(position_to_send, time_to_send)
            time.sleep(update_interval)
