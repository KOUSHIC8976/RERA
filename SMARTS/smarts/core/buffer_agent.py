             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
import abc
from abc import abstractmethod

from smarts.zoo.agent_spec import AgentSpec


class BufferAgent(metaclass=abc.ABCMeta):
    """An agent which is part of a buffer."""

    @abstractmethod
    def act(self, obs):
        """Gives a future action based on observations."""
        raise NotImplementedError

    @abstractmethod
    def start(self, agent_spec: AgentSpec):
        """Begin operation of this agent."""
        raise NotImplementedError

    @abstractmethod
    def terminate(self):
        """Clean up agent resources."""
        raise NotImplementedError
