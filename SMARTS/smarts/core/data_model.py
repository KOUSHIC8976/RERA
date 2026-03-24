                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Optional

from smarts.zoo.registry import make

if TYPE_CHECKING:
    from smarts.zoo.agent_spec import AgentSpec


@dataclass
class SocialAgent:
    """A serializable representation of a social agent."""

    id: str
    actor_name: str
    is_boid: bool
    is_boid_keep_alive: bool
    agent_locator: str
    policy_kwargs: Dict[str, Any] = field(default_factory=dict)
    initial_speed: Optional[float] = None

    def to_agent_spec(self) -> AgentSpec:
        """Generate an agent spec."""
        return make(locator=self.agent_locator, **self.policy_kwargs)
