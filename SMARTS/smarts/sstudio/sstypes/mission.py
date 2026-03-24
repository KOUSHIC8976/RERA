             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import sys
import warnings
from dataclasses import dataclass
from typing import Optional, Tuple, Union

from smarts.sstudio.sstypes.constants import MISSING
from smarts.sstudio.sstypes.entry_tactic import EntryTactic
from smarts.sstudio.sstypes.route import JunctionEdgeIDResolver, RandomRoute, Route


@dataclass(frozen=True)
class Via:
    """A point on a road that an actor must pass through"""

    road_id: Union[str, JunctionEdgeIDResolver]
    """The road this via is on"""
    lane_index: int
    """The lane this via sits on"""
    lane_offset: int
    """The offset along the lane where this via sits"""
    required_speed: float
    """The speed that a vehicle should travel through this via"""
    hit_distance: float = -1
    """The distance at which this waypoint can be hit. Negative means half the lane radius."""


@dataclass(frozen=True)
class Mission:
    """The descriptor for an actor's mission."""

    route: Union[RandomRoute, Route]
    """The route for the actor to attempt to follow."""

    via: Tuple[Via, ...] = ()
    """Points on an road that an actor must pass through"""

    start_time: float = MISSING
    """The earliest simulation time that this mission starts but may start later in couple with
    `entry_tactic`.
    """

    entry_tactic: Optional[EntryTactic] = None
    """A specific tactic the mission should employ to start the mission."""

    def __post_init__(self):
        if self.start_time != sys.maxsize:
            warnings.warn(
                "`start_time` is deprecated. Instead use `entry_tactic=EntryTactic(start_time=...)`.",
                category=DeprecationWarning,
            )


@dataclass(frozen=True)
class EndlessMission:
    """The descriptor for an actor's mission that has no end."""

    begin: Tuple[str, int, float]
    """The (road, lane_index, offset) details of the start location for the route.

    road:
        The starting road by name.
    lane_index:
        The lane index from the rightmost lane.
    offset:
        The offset in meters into the lane. Also acceptable\\: 'max', 'random'
    """
    via: Tuple[Via, ...] = ()
    """Points on a road that an actor must pass through"""
    start_time: float = MISSING
    """The earliest simulation time that this mission starts"""
    entry_tactic: Optional[EntryTactic] = None
    """A specific tactic the mission should employ to start the mission"""

    def __post_init__(self):
        if self.start_time != sys.maxsize:
            warnings.warn(
                "`start_time` is deprecated. Instead use `entry_tactic=EntryTactic(start_time=...)`.",
                category=DeprecationWarning,
            )


@dataclass(frozen=True)
class LapMission:
    """The descriptor for an actor's mission that defines mission that repeats
    in a closed loop.
    """

    route: Route
    """The route for the actor to attempt to follow"""
    num_laps: int
    """The amount of times to repeat the mission"""
    via: Tuple[Via, ...] = ()
    """Points on a road that an actor must pass through"""
    start_time: float = MISSING
    """The earliest simulation time that this mission starts"""
    entry_tactic: Optional[EntryTactic] = None
    """A specific tactic the mission should employ to start the mission"""

    def __post_init__(self):
        if self.start_time != sys.maxsize:
            warnings.warn(
                "`start_time` is deprecated. Instead use `entry_tactic=EntryTactic(start_time=...)`.",
                category=DeprecationWarning,
            )


@dataclass(frozen=True)
class GroupedLapMission:
    """The descriptor for a group of actor missions that repeat in a closed loop."""

    route: Route
    """The route for the actors to attempt to follow"""
    offset: int
    """The offset of the "starting line" for the group"""
    lanes: int
    """The number of lanes the group occupies"""
    actor_count: int
    """The number of actors to be part of the group"""
    num_laps: int
    """The amount of times to repeat the mission"""
    via: Tuple[Via, ...] = ()
    """Points on a road that an actor must pass through"""
    entry_tactic: Optional[EntryTactic] = None
    """A specific tactic the mission should employ to start the mission"""
