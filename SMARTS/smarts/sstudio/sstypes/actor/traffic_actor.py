             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


from dataclasses import dataclass, field
from typing import Union

from smarts.core.utils.file import pickle_hash_int
from smarts.sstudio.sstypes.actor import Actor
from smarts.sstudio.sstypes.distribution import Distribution
from smarts.sstudio.sstypes.traffic_model import JunctionModel, LaneChangingModel


@dataclass(frozen=True)
class TrafficActor(Actor):
    """Used as a description/spec for traffic actors (e.x. Vehicles, Pedestrians,
    etc). The defaults provided are for a car, but the name is not set to make it
    explicit that you actually want a car.
    """

    accel: float = 2.6
    """The maximum acceleration value of the actor (in m/s^2)."""
    decel: float = 4.5
    """The maximum deceleration value of the actor (in m/s^2)."""
    tau: float = 1.0
    """The minimum time headway"""
    sigma: float = 0.5
    """The driver imperfection"""                                                 
    depart_speed: Union[float, str] = "max"
    """The starting speed of the actor"""
    emergency_decel: float = 4.5
    """maximum deceleration ability of vehicle in case of emergency"""
    speed: Distribution = Distribution(mean=1.0, sigma=0.1)
    """The speed distribution of this actor in m/s."""
    imperfection: Distribution = Distribution(mean=0.5, sigma=0)
    """Driver imperfection within range [0..1]"""
    min_gap: Distribution = Distribution(mean=2.5, sigma=0)
    """Minimum gap (when standing) in meters."""
    max_speed: float = 55.5
    """The vehicle's maximum velocity (in m/s), defaults to 200 km/h for vehicles"""
    vehicle_type: str = "passenger"
    """The configured vehicle type this actor will perform as. ("passenger", "bus", "coach", "truck", "trailer")"""
    lane_changing_model: LaneChangingModel = field(
        default_factory=LaneChangingModel, hash=False
    )
    junction_model: JunctionModel = field(default_factory=JunctionModel, hash=False)

    def __hash__(self) -> int:
        return pickle_hash_int(self)

    @property
    def id(self) -> str:
        """The identifier tag of the traffic actor."""
        return "{}-{}".format(self.name, str(hash(self))[:6])
