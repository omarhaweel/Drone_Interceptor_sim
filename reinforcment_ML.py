import numpy as np
import random


actions = ["up", "down", "left", "right", "forward", "backward"]
alfa = 0.1
gamma = 0.9
epsilon = 0.1
episodes = 300

# goal changes dynamically and is the target drone position
goal = np.array([0, 0, 0], dtype=float)  # Initial goal position
start = np.array([0, 0, 0], dtype=float)  # Initial interceptor position


def is_terminal_state(current_interceptor_position, goal):
    distance = np.linalg.norm(current_interceptor_position - goal)
    return (
        distance < 1.0
    )  # detonation if interceptor is close enough to the target drone


# the next state is the next position to gather byu interceptor after choosing an action
def get_next_state(action, current_interceptor_position):
    """Calculate the next state based on the action taken."""
    if action == "up":
        return current_interceptor_position + np.array([0, 0, 1])
    elif action == "down":
        return current_interceptor_position - np.array([0, 0, 1])
    elif action == "left":
        return current_interceptor_position - np.array([1, 0, 0])
    elif action == "right":
        return current_interceptor_position + np.array([1, 0, 0])
    elif action == "forward":
        return current_interceptor_position + np.array([0, 1, 0])
    elif action == "backward":
        return current_interceptor_position - np.array([0, 1, 0])
    else:
        raise ValueError("Invalid action")


def get_reward(current_interceptor_position, goal):
    """Calculate the reward based on the current interceptor position and goal."""
    distance = np.linalg.norm(current_interceptor_position - goal)
    if distance < 1.0:
        return 100
    else:
        return -distance


# TODO: Implement Q-learning algorithm, get the live drone position and update the goal dynamically,
# let the interceptor learn to intercept the drone by updating its position based on the Q-values and the actions taken.
# against the drone dynamic position. LET's SEE IF WE CAN GET THE INTERCEPTOR TO LEARN TO INTERCEPT THE MOVING DRONE
