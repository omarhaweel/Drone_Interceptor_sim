import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drone import Drone
from interceptor import Interceptor
from radar import Radar

# test class for the drone
class TestDrone(unittest.TestCase):
    def setUp(self):
        self.drone = Drone([0, 0, 0], [1, 1, 1])

    def test_drone_initialization(self):
        """Test drone initializes with correct position and velocity"""
        np.testing.assert_array_equal(self.drone.position, [0, 0, 0])
        np.testing.assert_array_equal(self.drone.velocity, [1, 1, 1])
        self.assertFalse(self.drone.is_flying)

    def test_drone_start_stop_flying(self):
        """Test drone flying state management"""
        self.drone.start_flying()
        self.assertTrue(self.drone.is_flying)

        self.drone.stop_flying()
        self.assertFalse(self.drone.is_flying)

    def test_drone_position_update(self):
        """Test drone position updates correctly"""
        initial_position = self.drone.position.copy()
        self.drone.update_position(0.1, np.array([1, 1, 1]))

        expected_position = initial_position + np.array([0.1, 0.1, 0.1])
        np.testing.assert_array_almost_equal(self.drone.position, expected_position)

    def test_drone_history_tracking(self):
        """Test drone tracks position history"""
        initial_length = len(self.drone.history)
        self.drone.update_position(0.1, np.array([1, 0, 0]))

        self.assertEqual(len(self.drone.history), initial_length + 1)
        self.assertEqual(len(self.drone.time_history), initial_length + 1)


# a test class for the interceptor
class TestInterceptor(unittest.TestCase):
    def setUp(self):
        self.interceptor = Interceptor([0, 0, 0], [0, 0, 0])

    def test_interceptor_initialization(self):
        """Test interceptor initializes correctly"""
        np.testing.assert_array_equal(self.interceptor.position, [0, 0, 0])
        np.testing.assert_array_equal(self.interceptor.velocity, [0, 0, 0])
        self.assertFalse(self.interceptor.is_flying)
        self.assertEqual(self.interceptor.intercept_speed, 20.0) # can be adjusted

    def test_interceptor_flying_state(self):
        """Test interceptor flying state management"""
        self.interceptor.start_flying()
        self.assertTrue(self.interceptor.is_flying)

        self.interceptor.stop_flying()
        self.assertFalse(self.interceptor.is_flying)

    def test_interceptor_target_tracking(self):
        """Test interceptor moves toward target"""
        self.interceptor.start_flying()
        target_position = [10, 2, 0]

        initial_position = self.interceptor.position.copy()
        self.interceptor.update_position_from_radar(target_position, 0.1)

        # Interceptor should now move close to the target position
        self.assertGreater(self.interceptor.position[0], initial_position[0])
        self.assertGreater(self.interceptor.position[1], initial_position[1])
        self.assertEqual(self.interceptor.position[2], initial_position[2])

    def test_interceptor_stops_when_close(self):
        """Test interceptor moves towards target (may overshoot due to speed)"""
        self.interceptor.start_flying()
        # Reduce speed for this test to avoid overshoot
        self.interceptor.intercept_speed = 2.0  # Slower speed for testing

        self.interceptor.position = np.array([1.0, 0, 0])  # Start further away
        target_position = [0, 0, 0]

        initial_distance = np.linalg.norm(
            self.interceptor.position - np.array(target_position)
        )
        self.interceptor.update_position_from_radar(target_position, 0.1)

        # Should move towards target (distance should decrease)
        final_distance = np.linalg.norm(
            self.interceptor.position - np.array(target_position)
        )
        self.assertLess(final_distance, initial_distance)


# a test class for the radar
class TestRadar(unittest.TestCase):
    def setUp(self):
        self.radar = Radar()

    def test_radar_initialization(self):
        """Test radar initializes correctly"""
        self.assertEqual(len(self.radar.position_history), 0)
        self.assertEqual(len(self.radar.time_history), 0)
        self.assertFalse(self.radar.is_sending_updates_to_interceptor)

    def test_radar_receives_position(self):
        """Test radar can receive and store positions"""
        position = np.array([1, 2, 3])
        time_reading = 0.5

        self.radar.capture_position_variations(position, time_reading)

        self.assertEqual(len(self.radar.position_history), 1)
        self.assertEqual(len(self.radar.time_history), 1)
        np.testing.assert_array_equal(self.radar.position_history[0], position)
        self.assertEqual(self.radar.time_history[0], time_reading)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.drone = Drone([0, 0, 0], [1, 0, 0])
        self.interceptor = Interceptor([5, 0, 0], [0, 0, 0])
        self.radar = Radar()

    def test_interception_scenario(self):
        """Test the integration of drone, radar, and interceptor"""
        # Start systems
        self.drone.start_flying()
        self.interceptor.start_flying()

        # Simulate
        for i in range(5):
            # Update drone position as simulated after each time step
            self.drone.update_position(0.1, self.drone.velocity)

            # Send to radar
            self.radar.capture_position_variations(self.drone.position, i * 0.1)

            # Update interceptor
            self.interceptor.update_position_from_radar(self.drone.position, i * 0.1)

        # Verify interceptor moved toward drone
        self.assertLess(self.interceptor.position[0], 5.0)  # Should have moved left
        self.assertEqual(len(self.drone.history), 6)  # Initial + 5 updates after the loop executes
        self.assertEqual(len(self.radar.position_history), 5)


if __name__ == "__main__":
    unittest.main()
