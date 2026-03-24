             

                                                                        

                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          

                                                                            
                                                     

                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from collections import deque
from dataclasses import fields
from typing import Callable, Optional, Tuple, TypeVar, Union

import numpy as np

from smarts.env.gymnasium.wrappers.metric.types import Costs, Counts

T = TypeVar("T", Costs, Counts)


def add_dataclass(first: T, second: T) -> T:
    """Sums the fields of two `dataclass` objects.

    Args:
        first (T): First `dataclass` object.
        second (T): Second `dataclass` object.

    Returns:
        T: New summed `dataclass` object.
    """
    assert type(first) is type(second)
    new = {}
    for field in fields(first):
        new[field.name] = getattr(first, field.name) + getattr(second, field.name)
    output = first.__class__(**new)

    return output


def op_dataclass(
    first: T,
    second: Union[int, float],
    op: Callable[[Union[int, float], Union[int, float]], float],
) -> T:
    """Performs operation `op` on the fields of the source `dataclass` object.

    Args:
        first (T): The source `dataclass` object.
        second (Union[int, float]): Value input for the operator.
        op (Callable[[Union[int, float], Union[int, float]], float]): Operation to be performed.

    Returns:
        T: A new `dataclass` object with operation performed on all of its fields.
    """
    new = {}
    for field in fields(first):
        new[field.name] = op(getattr(first, field.name), second)
    output = first.__class__(**new)

    return output


def divide(value: Union[int, float], divider: Union[int, float]) -> float:
    """Division operation.

    Args:
        value (Union[int, float]): Numerator
        divider (Union[int, float]): Denominator

    Returns:
        float: Numerator / Denominator
    """
    return float(value / divider)


def multiply(value: Union[int, float], multiplier: Union[int, float]) -> float:
    """Multiplication operation.

    Args:
        value (Union[int, float]): Value
        multiplier (Union[int, float]): Multiplier

    Returns:
        float: Value x Multiplier
    """
    return float(value * multiplier)


def nearest_waypoint(
    matrix: np.ma.MaskedArray, points: np.ndarray, radius: float = 1
) -> Tuple[Tuple[int, int], Optional[int]]:
    """
    Returns
        (i) the `matrix` index of the nearest waypoint to the ego, which has a nearby `point`.
        (ii) the `points` index which is nearby the nearest waypoint to the ego.

    Nearby is defined as a point within `radius` of a waypoint.

    Args:
        matrix (np.ma.MaskedArray): Waypoints matrix.
        points (np.ndarray): Points matrix.
        radius (float, optional): Nearby radius. Defaults to 2.

    Returns:
        Tuple[Tuple[int, int], Optional[int]] : `matrix` index of shape (a,b) and scalar `point` index.
    """
    cur_point_index = ((np.int32(1e10), np.int32(1e10)), None)

    if points.shape == (0,):
        return cur_point_index

    assert len(matrix.shape) == 3
    assert matrix.shape[2] == 3
    assert len(points.shape) == 2
    assert points.shape[1] == 3

    points_expanded = np.expand_dims(points, (1, 2))
    diff = matrix - points_expanded
    dist = np.linalg.norm(diff, axis=-1)
    dist_masked = np.ma.MaskedArray(dist, diff.mask[..., 0])
    for ii in range(points.shape[0]):
        index = np.argmin(dist_masked[ii])
        index_unravel = np.unravel_index(index, dist_masked[ii].shape)
        min_dist = dist_masked[ii][index_unravel]
        if min_dist <= radius and index_unravel[1] < cur_point_index[0][1]:
            cur_point_index = (index_unravel, ii)

    return cur_point_index


class SlidingWindow:
    """A sliding window which moves to the right by accepting new elements. The
    maximum value within the sliding window can be queried at anytime by calling
    the max() method.
    """

    def __init__(self, size: int):
        """
        Args:
            size (int): Size of the sliding window.
        """
        self._values = deque(maxlen=size)
        self._max_candidates = deque(maxlen=size)
        self._size = size
        self._time = -1

    def move(self, x: Union[int, float]):
        """Moves the sliding window one step to the right by appending the new
        element x and discarding the oldest element on the left.

        Args:
            x (Union[int,float]): New element input to the sliding window.
        """
        self._time += 1

                                                                                
                                                     
        if len(self._values) == self._size:
            if self._values[0][0] == self._max_candidates[0][0]:
                self._max_candidates.popleft()
                                   
        self._values.append((self._time, x))

                                                                                 
        while self._max_candidates and self._max_candidates[-1][1] < x:
            self._max_candidates.pop()
                                           
        self._max_candidates.append((self._time, x))

    def max(self):
        """Returns the maximum element within the sliding window."""
        return self._max_candidates[0][1]

    def display(self):
        """Print the contents of the sliding window."""
        print("[", end="")
        for i in self._values:
            print(i, end=" ")
        print("]")
