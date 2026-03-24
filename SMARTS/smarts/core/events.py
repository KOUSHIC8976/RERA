                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, NamedTuple, Tuple

if TYPE_CHECKING:
    from smarts.core.vehicle_state import Collision


class Events(NamedTuple):
    """Classified observations that can trigger agent done status."""

    collisions: Tuple[Collision]
    """Collisions with other vehicles (if any)."""
    off_road: bool
    """True if vehicle is off the road, else False."""
    off_route: bool
    """True if vehicle is off the mission route, else False."""
    on_shoulder: bool
    """True if vehicle goes on road shoulder, else False."""
    wrong_way: bool
    """True if vehicle is heading against the legal driving direction of the lane, else False."""
    not_moving: bool
    """True if vehicle has not moved for the configured amount of time, else False."""
    reached_goal: bool
    """True if vehicle has reached its mission goal, else False."""
    reached_max_episode_steps: bool
    """True if vehicle has reached its max episode steps, else False."""
    agents_alive_done: bool
    """True if all configured co-simulating agents are done (if any), else False. 
    This is useful for cases when the vehicle is related to other vehicles."""
    interest_done: bool
    """True if described actors have left the simulation."""

    @property
    def actors_alive_done(self):
        """Deprecated. Use interest_done."""
        warnings.warn("Use interest_done.", category=DeprecationWarning)
        return self.interest_done
