             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from typing import Dict

import gymnasium as gym
import pytest

from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.scenario import Scenario
from smarts.core.utils.episodes import episodes
from smarts.env.gymnasium.hiway_env_v1 import HiWayEnvV1

AGENT_ID = "Agent-007"
MAX_EPISODES = 3


@pytest.fixture
def agent_interfaces():
    return {AGENT_ID: AgentInterface.from_type(AgentType.Laner, max_episode_steps=100)}


@pytest.fixture
def env(agent_interfaces: Dict[str, AgentInterface]):
    env: HiWayEnvV1 = gym.make(
        "smarts.env:hiway-v1",
        scenarios=["scenarios/sumo/loop"],
        agent_interfaces=agent_interfaces,
        action_options="unformatted",
        observation_options="unformatted",
        headless=True,
        fixed_timestep_sec=0.01,
        disable_env_checker=True,
    )
    yield env
    env.close()


def test_hiway_env_v1_type(env: gym.Env):
                                                              
    assert isinstance(env.unwrapped, HiWayEnvV1)
                      
    assert isinstance(env.unwrapped, gym.Env)


def test_hiway_env_v1_interface_generation(
    env: HiWayEnvV1, agent_interfaces: Dict[str, AgentInterface]
):
    agent_ids = set(agent_interfaces)
    assert agent_ids == set(env.agent_interfaces)
    assert all([env.agent_interfaces[k] == agent_interfaces[k] for k in agent_ids])
    assert not (agent_ids - env.agent_ids)


def test_hiway_env_v1_unformatted(env: HiWayEnvV1):
    episode = None
    for episode in episodes(n=MAX_EPISODES):
        observations = env.reset()
        episode.record_scenario(env.scenario_log)

        terminateds = {"__all__": False}
        while not terminateds["__all__"]:
            observations, rewards, terminateds, truncateds, infos = env.step(
                {AGENT_ID: "keep_lane"}
            )

                                                                               
                                                                               
                                                                             
                                             
            assert isinstance(rewards, dict)
            assert all(
                [-3 < reward < 3 for reward in rewards.values()]
            ), f"Expected bounded reward per timestep, but got {rewards}."

            episode.record_step(observations, rewards, terminateds, truncateds, infos)

    assert episode is not None and episode.index == (
        MAX_EPISODES - 1
    ), "Simulation must cycle through to the final episode."


def test_hiway_env_v1_reset_with_scenario(env: HiWayEnvV1):
    scenarios = ["scenarios/sumo/figure_eight"]
    scenario: Scenario = next(Scenario.scenario_variations(scenarios, [AGENT_ID]))

    env.reset(options={"scenario": scenario, "start_time": 1000})
    assert "figure_eight" in env.smarts.scenario.root_filepath
    assert env.smarts.elapsed_sim_time >= 1000
    env.step({AGENT_ID: "keep_lane"})
