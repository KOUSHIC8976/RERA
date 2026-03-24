             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from smarts.core.road_map import RoadMap

                                        
@dataclass(frozen=True)
class SimulationLocalConstants:
    """This is state that should only change every reset."""

    road_map: RoadMap
    road_map_hash: int

    def __eq__(self, __o: object) -> bool:
        if __o is None:
            return False
        assert isinstance(__o, SimulationLocalConstants)
        return self.road_map_hash == __o.road_map_hash
