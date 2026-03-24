                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               

import math


def time_to_cover(dist: float, speed: float, acc: float = 0.0) -> float:
    """
    Returns the time for a moving object traveling at
    speed and accelerating at acc to cover distance dist.
    Assumes that all units are consistent (for example,
    if distance is in meters, speed is in m/s).
    The returned value will be non-negative
    (but may be math.inf under some circumstances).
    """
    if dist == 0:
        return 0
    if abs(acc) < 1e-9:
        if speed == 0:
            return math.inf
        t = dist / speed
        return t if t >= 0 else math.inf
    discriminant = speed**2 + 2 * acc * dist
    if discriminant < 0:
        return math.inf
    rad = math.sqrt(discriminant)
    t1 = (rad - speed) / acc
    t2 = -(rad + speed) / acc
    mnt = min(t1, t2)
    if mnt >= 0:
        return mnt
    mxt = max(t1, t2)
    if mxt >= 0:
        return mxt
    return math.inf


def distance_covered(time: float, speed: float, acc: float = 0.0) -> float:
    """
    Returns the amount of distance covered by an object
    moving at speed and accelerating with acc.
    Assumes that all units are consistent (for example,
    if distance is in meters, speed is in m/s).
    """
    return time * (speed + 0.5 * acc * time)


def stopping_time(start_speed: float, deceleration: float) -> float:
    """
    Returns the time it would take to stop from initial speed start_speed
    by decelerating at a constant rate of deceleration.
    Note that deceleration should be a non-negative value (not a negative acceleration).
    """
    assert deceleration >= 0.0
    if deceleration == 0.0:
        return math.inf
    return start_speed / deceleration


def stopping_distance(start_speed: float, deceleration: float) -> float:
    """
    Returns the distance it would take to stop from initial speed start_speed
    by decelerating at a constant rate of deceleration.
    Note that deceleration should be a non-negative value (not a negative acceleration).
    """
    assert deceleration >= 0.0
    return 0.5 * start_speed * stopping_time(start_speed, deceleration)
