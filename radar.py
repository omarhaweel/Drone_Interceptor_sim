from threading import Thread
import time
from drone import Drone
import numpy as np


class Radar:
    def __init__(self):
        self.position_history = []
        self.time_history = []

        self.is_sending_updates_to_interceptor = False
        self.interceptor_update_thread = None
        self.interceptor = None
    
    def capture_position_variations(self, position, time_reading):
        self.position_history.append(position.copy())
        self.time_history.append(time_reading)
        print(f"[RADAR] Received drone position and time: {position} at time {time_reading:.2f}s")

    def start_sending_updates_to_interceptor(self, interceptor, update_interval):
        self.interceptor = interceptor
        if not self.is_sending_updates_to_interceptor:
            self.is_sending_updates_to_interceptor = True
            print("[RADAR] Starting to send updates to interceptor")
            self.interceptor_update_thread = Thread(target=self._send_updates_to_interceptor, args=(update_interval,))
            self.interceptor_update_thread.daemon = True 
            self.interceptor_update_thread.start()


    def _send_updates_to_interceptor(self, update_interval):
        while self.is_sending_updates_to_interceptor:
            if self.interceptor:
                # Send the latest position to the interceptor
                latest_position = self.position_history[-1]
                latest_time = self.time_history[-1]
                print(f"[RADAR] Sending position to interceptor: {latest_position} at time {latest_time:.2f}s")
                self.interceptor.update_position_from_radar(latest_position, latest_time)
            time.sleep(update_interval)
    
    def stop_sending_updates(self):
        self.is_sending_updates_to_interceptor = False
        if self.interceptor_update_thread:
            self.interceptor_update_thread.join()
        print("[RADAR] Stopped sending updates to interceptor")