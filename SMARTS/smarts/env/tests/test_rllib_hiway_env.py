             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from pathlib import Path

import gymnasium as gym
import numpy as np
import pytest

from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.env.rllib_hiway_env import RLlibHiWayEnv
from smarts.zoo.agent_spec import AgentSpec

AGENT_ID = "Agent-007"


@pytest.fixture
def rllib_agent():
    return {
        "agent_spec": AgentSpec(
            interface=AgentInterface.from_type(
                AgentType.Standard,
                                                                        
                max_episode_steps=10,
            ),
        ),
        "action_space": gym.spaces.Box(
            low=np.array([0.0, 0.0, -1.0]),
            high=np.array([1.0, 1.0, 1.0]),
            dtype=np.float32,
        ),
    }


def test_rllib_hiway_env(rllib_agent):
                                                                     
    scenario_path = Path(__file__).parent / "../../../scenarios/sumo/loop"

    env_config = {
        "scenarios": [str(scenario_path.absolute())],
        "seed": 42,
        "headless": True,
        "agent_specs": {AGENT_ID: rllib_agent["agent_spec"]},
    }

    class atdict(dict):
        __getattr__ = dict.__getitem__
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    env = RLlibHiWayEnv(config=atdict(**env_config, worker_index=0, vector_index=1))
    agent_ids = env.get_agent_ids()
    assert isinstance(agent_ids, set)
    assert AGENT_ID in agent_ids
    print(env.observation_space)

    term = {"__all__": False}
    env.reset()
    while not term["__all__"]:
        _, _, term, _, _ = env.step(
            {aid: rllib_agent["action_space"].sample() for aid in agent_ids}
        )
    env.close()
