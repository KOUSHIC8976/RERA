             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import pytest

from smarts.core.controllers import ActionSpaceType
from smarts.core.utils.dummy import dummy_observation


@pytest.fixture
def large_observation():
    return dummy_observation()


@pytest.fixture
def adapter_data():
    return [
        (ActionSpaceType.ActuatorDynamic, [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]),
        (ActionSpaceType.Continuous, [0.9, 0.8, 0.7], [0.9, 0.8, 0.7]),
        (ActionSpaceType.Lane, "keep_lane", "keep_lane"),
        (ActionSpaceType.LaneWithContinuousSpeed, [0, 20.2], [0, 20.2]),
        (
            ActionSpaceType.Trajectory,
            (
                [1, 2],
                [5, 6],
                [0.3, 3.14],
                [20.0, 21.0],
            ),
            (
                [166.23485529, 167.23485529],
                [2.2, 1.2],
                [-1.27079633, 1.56920367],
                [20.0, 21.0],
            ),
        ),
        (
            ActionSpaceType.TrajectoryWithTime,
            [
                [1, 2],
                [5, 6],
                [0.3, 3.14],
                [20.0, 21.0],
                [0.1, 0.2],
            ],
            [
                [166.23485529, 167.23485529],
                [2.2, 1.2],
                [-1.27079633, 1.56920367],
                [20.0, 21.0],
                [0.1, 0.2],
            ],
        ),
        (
            ActionSpaceType.MPC,
            [
                [1, 2],
                [5, 6],
                [0.3, 3.14],
                [20.0, 21.0],
            ],
            [
                [166.23485529, 167.23485529],
                [2.2, 1.2],
                [-1.27079633, 1.56920367],
                [20.0, 21.0],
            ],
        ),
        (
            ActionSpaceType.TargetPose,
            (2, 4, -2.9, 20),
            (165.23485529, 1.2, 1.81238898, 20.0),
        ),
        (ActionSpaceType.Direct, (2, 2), (2, 2)),
    ]
