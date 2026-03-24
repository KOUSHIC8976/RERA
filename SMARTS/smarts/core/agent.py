                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import logging
import warnings
from abc import ABCMeta, abstractmethod
from typing import Any, Callable

logger = logging.getLogger(__name__)


class Agent(metaclass=ABCMeta):
    """The base class for agents"""

    @classmethod
    def from_function(cls, agent_function: Callable[[Any], Any]) -> "Agent":
        """A utility function to create an agent from a lambda or other callable object.

        .. code-block:: python

            keep_lane_agent = Agent.from_function(lambda obs: "keep_lane")
        """
        return FunctionAgent(agent_function)

    @abstractmethod
    def act(self, obs, **configs):
        """The agent action. See documentation on observations, `AgentSpec`, and `AgentInterface`.

        Expects an adapted observation and returns a raw action.
        """

        raise NotImplementedError


class FunctionAgent(Agent):
    """An agent generated from a function."""

    def __init__(self, agent_function) -> None:
        assert callable(agent_function)
        self._agent_function = agent_function

    def act(self, obs, **configs):
        return self._agent_function(obs)


def deprecated_agent_spec(*args, **kwargs):
    """Deprecated version of AgentSpec, see smarts.zoo.agent_spec"""
    from smarts.zoo.agent_spec import AgentSpec as AgentSpecAlias

    warnings.warn(
        "The AgentSpec class has moved to the following module: smarts.zoo.agent_spec. Calling it from this module will be deprecated.",
        DeprecationWarning,
    )
    return AgentSpecAlias(*args, **kwargs)


AgentSpec = deprecated_agent_spec
