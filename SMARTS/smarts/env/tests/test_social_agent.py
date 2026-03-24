             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import gymnasium as gym
import pytest

from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.env.gymnasium.hiway_env_v1 import HiWayEnvV1
from smarts.env.utils.action_conversion import ActionOptions
from smarts.env.utils.observation_conversion import ObservationOptions

AGENT_ID = "Agent-007"
SOCIAL_AGENT_ID_PREFIX = "zoo"

MAX_EPISODES = 1


@pytest.fixture
def agent_interface():
    return AgentInterface.from_type(
        AgentType.Laner, max_episode_steps=100, neighborhood_vehicle_states=True
    )


@pytest.fixture
def env(agent_interface: AgentInterface):
    env = gym.make(
        "smarts.env:hiway-v1",
        scenarios=["scenarios/sumo/zoo_intersection"],
        agent_interfaces={AGENT_ID: agent_interface},
        headless=True,
        observation_options=ObservationOptions.unformatted,
        action_options=ActionOptions.unformatted,
    )

    yield env
    env.close()


def test_social_agents_not_in_env_obs_keys(env: HiWayEnvV1):
    for _ in range(MAX_EPISODES):
        observations = env.reset()

        terminateds = {"__all__": False}
        while not terminateds["__all__"]:
            observations, rewards, terminateds, truncateds, infos = env.step(
                {AGENT_ID: "keep_lane"}
            )
                      
            assert len([key for key in observations.keys() if SOCIAL_AGENT_ID_PREFIX in key])==0
            assert isinstance(terminateds,dict) and isinstance(truncateds,dict)
            assert len([key for key in terminateds.keys() if SOCIAL_AGENT_ID_PREFIX in key])==0
            assert len([key for key in truncateds.keys() if SOCIAL_AGENT_ID_PREFIX in key])==0
                     


def test_social_agents_in_env_neighborhood_vehicle_obs(env: HiWayEnvV1):
    first_seen_vehicles = {}
    for _ in range(MAX_EPISODES):
        observations, _ = env.reset()

        terminateds = {"__all__": False}
        while not terminateds["__all__"]:
            observations, rewards, terminateds, _, infos = env.step(
                {AGENT_ID: "keep_lane"}
            )

            new_nvs_ids = [
                nvs.id
                for nvs in observations[AGENT_ID].neighborhood_vehicle_states
                if nvs.id not in first_seen_vehicles
            ]
            for v_id in new_nvs_ids:
                first_seen_vehicles[v_id] = observations[AGENT_ID].step_count + 1

    seen_zoo_social_vehicles = [v_id for v_id in first_seen_vehicles if "zoo" in v_id]
    assert len(seen_zoo_social_vehicles) == 2
    late_entry = next(
        (v_id for v_id in seen_zoo_social_vehicles if "zoo-car1" in v_id), None
    )
    assert late_entry is not None, seen_zoo_social_vehicles
    assert first_seen_vehicles[late_entry] == 8
