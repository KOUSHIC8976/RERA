                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from smarts.core.coordinates import Dimensions, Pose


class ActorRole(IntEnum):
    """Used to specify the role an actor (e.g. vehicle) is currently playing in the simulation."""

    Unknown = 0

                   
    Social = 1           
    SocialAgent = 2
    EgoAgent = 3

                       
    Signal = 4

                                                                                  
                                            
    External = 5


@dataclass
class ActorState:
    """Actor state information."""

    actor_id: str                                        
    actor_type: Optional[str] = None
    source: Optional[str] = None                                              
    role: ActorRole = ActorRole.Unknown
    updated: bool = False

    def get_pose(self) -> Optional[Pose]:
        """Get the pose of this actor. Some actors do not have a physical location."""
        return None

    def get_dimensions(self) -> Optional[Dimensions]:
        """Get the dimensions of this actor. Some actors do not have physical dimensions."""
        return None

    def __lt__(self, other) -> bool:
        """Allows ordering ActorStates for use in sorted data-structures."""
        assert isinstance(other, ActorState)
        return self.actor_id < other.actor_id or (
            self.actor_id == other.actor_id and id(self) < id(other)
        )

    def __hash__(self) -> int:
                                                       
        return hash(self.actor_id)

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and hash(self.actor_id) == hash(
            other.actor_id
        )
