             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from typing import Dict

import gymnasium as gym
import numpy as np
import pytest

from smarts.core.agent_interface import RGB, AgentInterface
from smarts.core.controllers import ActionSpaceType
from smarts.env.gymnasium.wrappers.single_agent import SingleAgent
from smarts.env.utils.action_conversion import ActionOptions


def _make_agent_interfaces(num_agent):
    agent_interfaces: Dict[str, AgentInterface] = {
        "AGENT_"
        + str(agent_id): AgentInterface(
            top_down_rgb=RGB(),
            action=ActionSpaceType.Lane,
        )
        for agent_id in range(num_agent)
    }

    return agent_interfaces


class ObservationWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = {
            agent_id: agent_space["top_down_rgb"]
            for agent_id, agent_space in self.env.observation_space.items()
        }

    def observation(self, obs):
        return {
            agent_name: agent_obs["top_down_rgb"]
            for agent_name, agent_obs in obs.items()
        }


@pytest.fixture
def base_env(request):
    agent_interfaces = _make_agent_interfaces(request.param)
    env = gym.make(
        "smarts.env:hiway-v1",
        scenarios=["scenarios/sumo/figure_eight"],
        agent_interfaces=agent_interfaces,
        headless=True,
        action_options=ActionOptions.unformatted,
    )
    env = ObservationWrapper(env)

    yield env
    env.close()


@pytest.mark.parametrize("base_env", [1, 2], indirect=True)
def test_init(base_env):
                                                    
    ma_agent_interfaces = base_env.agent_interfaces
    ma_obs_space = base_env.observation_space

                                                                 
    if len(ma_agent_interfaces) > 1:
        with pytest.raises(AssertionError):
            env = SingleAgent(base_env)
            env.close()
        return
    else:
        env = SingleAgent(base_env)

                                
    agent_id = next(iter(ma_agent_interfaces.keys()))
    assert env.observation_space == ma_obs_space[agent_id]

    env.close()


@pytest.mark.parametrize("base_env", [1], indirect=True)
def test_reset_and_step(base_env):
    ma_agent_interfaces = base_env.agent_interfaces
    ma_obs, ma_info = base_env.reset()

    env = SingleAgent(base_env)
    single_obs, single_info = env.reset()

                            
    assert isinstance(single_obs, np.ndarray)
    agent_id = next(iter(ma_agent_interfaces.keys()))
    assert single_obs.shape == ma_obs[agent_id].shape
    assert set(single_info.keys()) == set(ma_info[agent_id].keys())

                           
    ma_obs, _, _, _, ma_info = base_env.step({agent_id: "keep_lane"})
    (
        single_obs,
        single_reward,
        single_terminated,
        single_truncated,
        single_info,
    ) = env.step("keep_lane")
    assert isinstance(single_obs, np.ndarray)
    assert single_obs.shape == ma_obs[agent_id].shape
    assert isinstance(single_reward, float)
    assert type(single_terminated) is bool
    assert type(single_truncated) is bool
    assert set(single_info.keys()) == set(ma_info[agent_id].keys())

    env.close()
