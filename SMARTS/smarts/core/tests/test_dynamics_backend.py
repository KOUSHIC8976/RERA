             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math

import numpy as np
import pytest

from smarts.core.chassis import AckermannChassis
from smarts.core.coordinates import Heading, Pose
from smarts.core.utils import pybullet
from smarts.core.utils.pybullet import bullet_client as bc


@pytest.fixture
def bullet_client():
    client = bc.BulletClient(pybullet.DIRECT)
    yield client
    client.disconnect()


@pytest.fixture
def chassis(bullet_client):
    return AckermannChassis(
        Pose.from_center([0, 0, 0], Heading(math.pi * 0.5)), bullet_client
    )


def step_with_vehicle_commands(bv, steps, throttle=0, brake=0, steering=0):
    for _ in range(steps):
        bv.control(throttle, brake, steering)
        bv._client.stepSimulation()


def test_steering_direction(chassis):
    step_with_vehicle_commands(chassis, steps=100, steering=0)
    assert math.isclose(chassis.steering, 0, rel_tol=1e-2)

                                                                            
                                           
    step_with_vehicle_commands(chassis, steps=100, steering=1)
    assert chassis.steering > 0

                                                                           
                                          
    step_with_vehicle_commands(chassis, steps=100, steering=-1)
    assert chassis.steering < 0


def test_set_pose(chassis):
    chassis.set_pose(Pose.from_center([137, -5.8, 1], Heading(1.8)))
    position, heading = chassis.pose.position, chassis.pose.heading

    assert np.linalg.norm(np.subtract(position, np.array([137, -5.8, 1]))) < 1e-16
    assert np.isclose(heading, 1.8)
