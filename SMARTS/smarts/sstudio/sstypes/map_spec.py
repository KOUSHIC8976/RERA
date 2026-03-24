             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


                                                                          
                                                                            
                                                                               
 
                                                                                     
                                                                      
                                                          
from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple

from smarts.core.default_map_builder import get_road_map
from smarts.core.road_map import RoadMap

MapBuilder = Callable[[Any], Tuple[Optional[RoadMap], Optional[str]]]


@dataclass(frozen=True)
class MapSpec:
    """A map specification that describes how to generate a roadmap."""

    source: str
    """A path or URL or name uniquely designating the map source."""
    lanepoint_spacing: float = 1.0
    """The default distance between pre-generated Lane Points (Waypoints)."""
    default_lane_width: Optional[float] = None
    """If specified, the default width (in meters) of lanes on this map."""
    shift_to_origin: bool = False
    """If True, upon creation a map whose bounding-box does not intersect with
    the origin point (0,0) will be shifted such that it does."""
    builder_fn: MapBuilder = get_road_map
    """If specified, this should return an object derived from the RoadMap base class
    and a hash that uniquely identifies it (changes to the hash should signify
    that the map is different enough that map-related caches should be reloaded).
    The parameter is this MapSpec object itself.
    If not specified, this currently defaults to a function that creates
    SUMO road networks (get_road_map()) in smarts.core.default_map_builder."""
