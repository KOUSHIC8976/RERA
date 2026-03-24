                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

from concurrent import futures
from typing import TYPE_CHECKING

from smarts.core.buffer_agent import BufferAgent

if TYPE_CHECKING:
    from smarts.core.agent import Agent
    from smarts.zoo.agent_spec import AgentSpec


class LocalAgent(BufferAgent):
    """A local implementation of a buffer agent."""

    def __init__(self):
        self._agent: Agent = None
        self._agent_spec: AgentSpec = None

    def act(self, obs):
        """Call the agent's act function asynchronously and return a Future."""

        act_future = futures.Future()
        act_future.set_result(self._agent.act(obs))
        return act_future

    def start(self, agent_spec: AgentSpec):
        """Send the AgentSpec to the agent runner."""
        self._agent_spec = agent_spec
        self._agent = self._agent_spec.build_agent()

    def terminate(self):
        pass
