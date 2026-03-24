                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

from dataclasses import dataclass
from enum import IntFlag
from typing import TYPE_CHECKING, List, Optional

from smarts.core.colors import SceneColors

from .actor import ActorState

if TYPE_CHECKING:
    from smarts.core import coordinates


class SignalLightState(IntFlag):
    """States that a traffic signal light may take;
    note that these may be combined into a bit-mask."""

    UNKNOWN = 0
    OFF = 0
    STOP = 1
    CAUTION = 2
    GO = 4
    FLASHING = 8
    ARROW = 16


def signal_state_to_color(state: SignalLightState) -> SceneColors:
    """Maps a signal state to a color."""
    if state == SignalLightState.STOP:
        return SceneColors.SignalStop
    elif state == SignalLightState.CAUTION:
        return SceneColors.SignalCaution
    elif state == SignalLightState.GO:
        return SceneColors.SignalGo
    else:
        return SceneColors.SignalUnknown


@dataclass
class SignalState(ActorState):
    """Traffic signal state information."""

    state: Optional[SignalLightState] = None
    stopping_pos: Optional[coordinates.Point] = None
    controlled_lanes: Optional[List[str]] = None
    last_changed: Optional[float] = None                             

    def __post_init__(self):
        assert self.state is not None
