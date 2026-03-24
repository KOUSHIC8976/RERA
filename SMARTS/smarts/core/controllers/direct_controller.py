                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math
from typing import Tuple, Union

import numpy as np

from smarts.core.chassis import AckermannChassis, BoxChassis
from smarts.core.coordinates import Pose
from smarts.core.utils.core_math import fast_quaternion_from_angle, radians_to_vec


class DirectController:
    """A controller that directly sets a vehicle's acceleration and angular velocity
    (rather than applying forces like torque) based on kinematics."""

    @classmethod
    def perform_action(
        cls,
        dt: float,
        vehicle,
        action: Union[float, Tuple[float, float]],
    ):
        """Performs an action adapting to the underlying chassis.
        Args:
            dt (float):
                A delta time value.
            vehicle (Vehicle):
                The vehicle to control.
            action (Union[float, Tuple[float, float]]):
                (speed) XOR (acceleration, angular_velocity)
        """
        chassis = vehicle.chassis
        if isinstance(action, (int, float)):
                                                      
            if isinstance(chassis, BoxChassis):
                vehicle.control(vehicle.pose, action, dt)
            elif isinstance(chassis, AckermannChassis):
                chassis.speed = action                                      
            return
        assert isinstance(action, (list, tuple)) and len(action) == 2

                                                                              
                                                               
        acceleration, angular_velocity = action

                                                                                    
                                                                             
                                                                                
        target_heading = (vehicle.heading + angular_velocity * dt) % (2 * math.pi)

        if isinstance(chassis, BoxChassis):
                                                                                                                 
                                                                                                         
            heading_vec = radians_to_vec(vehicle.heading)
            dpos = heading_vec * vehicle.speed * dt
            new_pose = Pose(
                position=vehicle.position + np.append(dpos, 0.0),
                orientation=fast_quaternion_from_angle(target_heading),
            )
            target_speed = vehicle.speed + acceleration * dt
            vehicle.control(new_pose, target_speed, dt)

        elif isinstance(chassis, AckermannChassis):
            mass = chassis.mass_and_inertia[0]         
            wheel_radius = chassis.wheel_radius
                                                                   
                                                                                                         
            if acceleration >= 0:
                                                             
                torque_ratio = mass / (4 * wheel_radius * chassis.max_torque)
                throttle = np.clip(acceleration * torque_ratio, 0, 1)
                brake = 0
            else:
                throttle = 0
                                                             
                torque_ratio = mass / (4 * wheel_radius * chassis.max_btorque)
                brake = np.clip(acceleration * torque_ratio, 0, 1)

            steering = np.clip(dt * -angular_velocity * chassis.steering_ratio, -1, 1)
            vehicle.control(throttle=throttle, brake=brake, steering=steering)

        else:
            raise Exception("unsupported chassis type")
