             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


from dataclasses import dataclass, field
from typing import Any, Optional, Tuple

from smarts.core import gen_id
from smarts.core.utils.file import pickle_hash_int
from smarts.sstudio.sstypes.map_spec import MapSpec


@dataclass(frozen=True)
class JunctionEdgeIDResolver:
    """A utility for resolving a junction connection edge"""

    start_edge_id: str
    start_lane_index: int
    end_edge_id: str
    end_lane_index: int

    def to_edge(self, sumo_road_network) -> str:
        """Queries the road network to see if there is a junction edge between the two
        given edges.
        """
        return sumo_road_network.get_edge_in_junction(
            self.start_edge_id,
            self.start_lane_index,
            self.end_edge_id,
            self.end_lane_index,
        )


@dataclass(frozen=True)
class Route:
    """A route is represented by begin and end road IDs, with an optional list of
    intermediary road IDs. When an intermediary is not specified the router will
    decide what it should be.
    """

                               
    begin: Tuple[str, int, Any]
    """The (road, lane_index, offset) details of the start location for the route.

    road:
        The starting road by name.
    lane_index:
        The lane index from the rightmost lane.
    offset:
        The offset in meters into the lane. Also acceptable\\: "max", "random"
    """
                               
    end: Tuple[str, int, Any]
    """The (road, lane_index, offset) details of the end location for the route.

    road:
        The starting road by name.
    lane_index:
        The lane index from the rightmost lane.
    offset:
        The offset in meters into the lane. Also acceptable\\: "max", "random"
    """

                                                    
    via: Tuple[str, ...] = field(default_factory=tuple)
    """The ids of roads that must be included in the route between `begin` and `end`."""

    map_spec: Optional[MapSpec] = None
    """All routes are relative to a road map.  If not specified here,
    the default map_spec for the scenario is used."""

    @property
    def id(self) -> str:
        """The unique id of this route."""
        return "{}-{}-{}".format(
            "_".join(map(str, self.begin)),
            "_".join(map(str, self.end)),
            str(hash(self))[:6],
        )

    @property
    def roads(self):
        """All roads that are used within this route."""
        return (self.begin[0],) + self.via + (self.end[0],)

    def __hash__(self):
        return pickle_hash_int(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and hash(self) == hash(other)


@dataclass(frozen=True)
class RandomRoute:
    """An alternative to types.Route which specifies to ``sstudio`` to generate a random
    route.
    """

    id: str = field(default_factory=lambda: f"random-route-{gen_id()}")

    map_spec: Optional[MapSpec] = None
    """All routes are relative to a road map.  If not specified here,
    the default map_spec for the scenario is used."""

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and hash(self) == hash(other)
