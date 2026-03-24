             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from smarts.core import gen_id
from smarts.sstudio.sstypes.actor import Actor
from smarts.sstudio.sstypes.bubble_limits import BubbleLimits


@dataclass(frozen=True)
class SocialAgentActor(Actor):
    """Used as a description/spec for zoo traffic actors. These actors use a
    pre-trained model to understand how to act in the environment.
    """

                                                                                  
                               
    agent_locator: str
    """The locator reference to the zoo registration call. Expects a string in the format
    of 'path.to.file:locator-name' where the path to the registration call is in the form
    `{PYTHONPATH}[n]/path/to/file.py`
    """
    policy_kwargs: Dict[str, Any] = field(default_factory=dict)
    """Additional keyword arguments to be passed to the constructed class overriding the
    existing registered arguments.
    """
    initial_speed: Optional[float] = None
    """Set the initial speed, defaults to 0."""


@dataclass(frozen=True)
class BoidAgentActor(SocialAgentActor):
    """Used as a description/spec for boid traffic actors. Boid actors control multiple
    vehicles.
    """

    id: str = field(default_factory=lambda: f"boid-{gen_id()}")

                                                                                      
                                                              
    capacity: Optional[BubbleLimits] = None
    """The capacity of the boid agent to take over vehicles."""
