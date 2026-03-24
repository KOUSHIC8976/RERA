             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from dataclasses import dataclass, field, replace
from typing import Dict, Optional, Sequence, Union

from smarts.core.utils.file import pickle_hash_int
from smarts.sstudio.sstypes.actor.traffic_actor import TrafficActor
from smarts.sstudio.sstypes.route import RandomRoute, Route


@dataclass(frozen=True)
class Flow:
    """A route with an actor type emitted at a given rate."""

    route: Union[RandomRoute, Route]
    """The route for the actor to attempt to follow."""
    rate: float
    """Vehicles per hour."""
    begin: float = 0
    """Start time in seconds."""
                                                                                     
                                                 
    end: float = 1 * 60 * 60
    """End time in seconds."""
    actors: Dict[TrafficActor, float] = field(default_factory=dict)
    """An actor to weight mapping associated as { actor -> weight }.

    :param actor: The traffic actors that are provided.
    :param weight: The chance of this actor appearing as a ratio over total weight.
    """
    randomly_spaced: bool = False
    """Determines if the flow should have randomly spaced traffic. Defaults to `False`."""
    repeat_route: bool = False
    """If True, vehicles that finish their route will be restarted at the beginning. Defaults to `False`."""

    @property
    def id(self) -> str:
        """The unique id of this flow."""
        return "{}-{}".format(
            self.route.id,
            str(hash(self))[:6],
        )

    def __hash__(self):
                                                                                   
                    
        return pickle_hash_int((self.route, self.rate, frozenset(self.actors.items())))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and hash(self) == hash(other)


@dataclass(frozen=True)
class Trip:
    """A route with a single actor type with name and unique id."""

    vehicle_name: str
    """The name of the vehicle. It must be unique. """
    route: Union[RandomRoute, Route]
    """The route for the actor to attempt to follow."""
    vehicle_type: str = "passenger"
    """The type of the vehicle"""
    depart: float = 0
    """Start time in seconds."""
    actor: Optional[TrafficActor] = field(default=None)
    """The traffic actor model (usually vehicle) that will be used for the trip."""

    def __post_init__(self):
        object.__setattr__(
            self,
            "actor",
            (
                replace(
                    self.actor, name=self.vehicle_name, vehicle_type=self.vehicle_type
                )
                if self.actor is not None
                else TrafficActor(
                    name=self.vehicle_name, vehicle_type=self.vehicle_type
                )
            ),
        )

    @property
    def id(self) -> str:
        """The unique id of this trip."""
        return self.vehicle_name

    def __hash__(self):
                                                                                   
                    
        return pickle_hash_int((self.route, self.actor))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and hash(self) == hash(other)


@dataclass(frozen=True)
class Traffic:
    """The descriptor for traffic."""

    flows: Sequence[Flow]
    """Flows are used to define a steady supply of vehicles."""
                                                                                   
                                                                                        
    trips: Optional[Sequence[Trip]] = None
    """Trips are used to define a series of single vehicle trip."""
    engine: str = "SUMO"
    """Traffic-generation engine to use. Supported values include "SUMO" and "SMARTS". "SUMO" requires using a SumoRoadNetwork for the RoadMap.
    """
