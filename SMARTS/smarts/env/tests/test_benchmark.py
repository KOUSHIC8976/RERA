             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import gymnasium as gym
import pytest

from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.controllers import ActionSpaceType


@pytest.fixture(params=[5, 10])
def agent_ids(request):
    return ["AGENT-{}".format(i) for i in range(request.param)]


@pytest.fixture(params=["laner", "rgb", "lidar"])
def agent_interface(request):
    if request.param == "laner":
        return AgentInterface.from_type(AgentType.Laner)
    if request.param == "rgb":
        return AgentInterface(top_down_rgb=True, action=ActionSpaceType.Lane)
    if request.param == "lidar":
        return AgentInterface(lidar_point_cloud=True, action=ActionSpaceType.Lane)


@pytest.fixture
def agent_interfaces(agent_ids, agent_interface):
    return {id_: agent_interface for id_ in agent_ids}


@pytest.fixture
def env(agent_specs):
    env = gym.make(
        "smarts.env:hiway-v1",
        scenarios=["scenarios/sumo/loop"],
        agent_interfaces=agent_interfaces,
        headless=True,
        seed=2008,
        fixed_timestep_sec=0.1,
    )
    env.reset()
    yield env
    env.close()


@pytest.mark.benchmark(group="env.step")
def test_benchmark_step(agent_ids, env, benchmark):
    @benchmark
    def env_step(counts=5):
        while counts:
            env.step({id_: "keep_lane" for id_ in agent_ids})
            counts -= 1
