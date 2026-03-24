             

                                                                        

                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          

                                                                            
                                                     

                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from dataclasses import dataclass


@dataclass(frozen=True)
class Costs:
    """Performance cost values."""

    collisions: int = 0
    comfort: float = 0
    dist_to_destination: float = 0
    dist_to_obstacles: float = 0
    jerk_linear: float = 0
    lane_center_offset: float = 0
    off_road: int = 0
    speed_limit: float = 0
    steps: float = 0
    vehicle_gap: float = 0
    wrong_way: float = 0


@dataclass(frozen=True)
class Counts:
    """Performance count values."""

    goals: int = 0
    """ Number of episodes completed successfully by achieving the goal.
    """
    episodes: int = 0
    """ Number of episodes traversed.
    """
    steps: int = 0
    """ Sum of steps taken over all episodes.
    """


@dataclass(frozen=True)
class Metadata:
    """Metadata of the record."""

    difficulty: float = 1
    """Task difficulty value.
    """


@dataclass
class Record:
    """Stores an agent's performance-cost, performance-count, and
    performance-metadata values."""

    costs: Costs
    counts: Counts
    metadata: Metadata
