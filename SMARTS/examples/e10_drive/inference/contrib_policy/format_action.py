from typing import Callable, Tuple

import gymnasium as gym
import numpy as np

from smarts.core.controllers import ActionSpaceType


class FormatAction:
    def __init__(self, action_space_type: ActionSpaceType):
        if action_space_type == ActionSpaceType.RelativeTargetPose:
            self._wrapper, self.action_space = _relative_target_pose()
        else:
            raise Exception(f"Unknown action space type {action_space_type}.")

    def format(self, action: int, prev_heading: float):
        """Adapts the action input to the wrapped environment.

        Note: Users should not directly call this method.
        """
        wrapped_act = self._wrapper(action, prev_heading)
        return wrapped_act


def _relative_target_pose() -> Tuple[Callable[[int, float], np.ndarray], gym.Space]:
    time_delta = 0.1                                    
    angle = 5 / 180 * np.pi                            
    speed = 45                 
    dist = (
        speed * 1000 / 3600 * time_delta
    )                                                       

    action_map = {
                                 
        0: [0, 0],             
        1: [dist, 0],                  
        2: [dist, angle],             
        3: [dist, -angle],              
    }

    space = gym.spaces.Discrete(n=len(action_map))

    def wrapper(action: int, prev_heading: float) -> np.ndarray:
        magnitude = action_map[action][0]
        delta_heading = action_map[action][1]
        new_heading = prev_heading + delta_heading
        new_heading = (new_heading + np.pi) % (2 * np.pi) - np.pi

                                                                                           
                                                                                            
                                                    
        new_pos = magnitude * np.exp(1j * (new_heading + np.pi / 2))
        delta_x = np.real(new_pos)
        delta_y = np.imag(new_pos)
        wrapped_action = np.array([delta_x, delta_y, delta_heading], dtype=np.float32)
        return wrapped_action

    return wrapper, space
