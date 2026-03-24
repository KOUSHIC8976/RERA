             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from typing import Any, Tuple

import gymnasium as gym


class SingleAgent(gym.Wrapper):
    """Converts a single-agent SMARTS environment's step and reset output to be
    compliant with gym spaces."""

    def __init__(self, env: gym.Env):
        """
        Args:
            env (gym.Env): Single-agent SMARTS environment to be wrapped.
        """
        super(SingleAgent, self).__init__(env)

        agent_ids = list(env.agent_interfaces.keys())
        assert (
            len(agent_ids) == 1
        ), f"Expected env to have a single agent, but got {len(agent_ids)} agents."
        self._agent_id = agent_ids[0]

        if self.observation_space:
            self.observation_space = self.observation_space[self._agent_id]

        if self.action_space:
            self.action_space = self.action_space[self._agent_id]

    def step(self, action: Any) -> Tuple[Any, float, bool, bool, Any]:
        """Steps a single-agent SMARTS environment.

        Args:
            action (Any): Agent's action

        Returns:
            Tuple[Any, float, bool, bool, Any]: Agent's observation, reward,
                terminated, truncated, and info
        """
        obs, reward, terminated, truncated, info = self.env.step(
            {self._agent_id: action}
        )
        return (
            obs[self._agent_id],
            reward[self._agent_id],
            terminated[self._agent_id],
            truncated[self._agent_id],
            info[self._agent_id],
        )

    def reset(self, *, seed=None, options=None) -> Tuple[Any, Any]:
        """Resets a single-agent SMARTS environment.

        Returns:
            Tuple[Any, Any]: Agent's observation and info
        """
        obs, info = self.env.reset(seed=seed, options=options)
        return obs[self._agent_id], info[self._agent_id]
