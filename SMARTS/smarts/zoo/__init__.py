                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math
import random

from smarts.core.agent import Agent
from smarts.core.agent_interface import ActionSpaceType, AgentInterface
from smarts.zoo.agent_spec import AgentSpec
from smarts.zoo.registry import register


class RandomRelativeTargetPoseAgent(Agent):
    """A simple agent that can move a random distance."""

    def __init__(self, speed=28, timestep=0.1) -> None:
        super().__init__()
        self._speed_per_step = speed / timestep

    def act(self, obs, **configs):
        return [
            (random.random() - 0.5) * self._speed_per_step,
            (random.random() - 0.5) * self._speed_per_step,
            random.random() * 2 * math.pi - math.pi,
        ]


                                                 
def entry_point(speed=10, **kwargs):
    """An example entrypoint for a simple agent.
    This can have any number of arguments similar to the gym environment standard.
    """
    return AgentSpec(
        AgentInterface(
            action=ActionSpaceType.RelativeTargetPose,
        ),
        agent_builder=RandomRelativeTargetPoseAgent,
        agent_params=dict(speed=speed),
    )


                                
register("random-relative-target-pose-agent-v0", entry_point)
