                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               
import abc
from typing import Optional

from smarts.core.buffer_agent import BufferAgent


class AgentBuffer(metaclass=abc.ABCMeta):
    """Defines a buffer of agents for external use."""

    @abc.abstractmethod
    def destroy(self):
        """Clean up the buffer resources."""
        raise NotImplementedError

    @abc.abstractmethod
    def acquire_agent(
        self, retries: int = 3, timeout: Optional[float] = None
    ) -> BufferAgent:
        """Get an agent from the buffer."""
        raise NotImplementedError
