                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
from typing import Any

import gymnasium as gym
import numpy as np

from smarts.core.sensors import Observation
from smarts.core.utils.file import smarts_local_user_dir
from smarts.env.wrappers.utils.rendering import vis_sim_obs

Action = Any
Operation = Any

default_log_dir = smarts_local_user_dir()


class AgentCameraRGBRender:
    """Wraps the environment with `rgb_array` render mode capabilities."""

    def __init__(self, env: gym.Env, max_agents: int = 1, enabled=True):
        self._max_agents = max_agents
        self._enabled = enabled
        self._image_frame = []
        self.is_vector_env = getattr(env, "is_vector_env", False)

    def step(self, obs, rewards, dones, infos):
        """Record a step."""

        single_env_obs = obs
        if self.is_vector_env:
                                                 
            single_env_obs = obs[0]

        self._record_for_render(single_env_obs)

    def render(self, mode="rgb_array", **kwargs):
        """Render the given camera image in this environment."""

        if len(self._image_frame) > 0:
            return self._image_frame

    def reset(self, obs) -> Any:
        """Record the reset of the environment."""

        self._record_for_render(obs)
        return obs

    def _record_for_render(self, obs) -> Any:
        if not self._enabled:
            return
        if isinstance(obs, Observation):
            obs = {"default_agent": obs}
        values = list(vis_sim_obs(obs).values())
        largest_image = max(values, key=lambda im: np.product(im.shape))
        image = np.array([np.resize(im, largest_image.shape) for im in values])
        if len(image.shape) > 2:
            self._image_frame = np.reshape(
                image,
                (
                    image.shape[0] * image.shape[2],
                    image.shape[1] * image.shape[3],
                    image.shape[4],
                ),
            )
