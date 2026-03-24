                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import numpy as np

METER_PER_SECOND_TO_KM_PER_HR = 3.6


class ActuatorDynamicControllerState:
    """Controller state information"""

    def __init__(self):
        self.last_steering_angle = 0


class ActuatorDynamicController:
    """A controller that maintains the last steering angle."""

    @classmethod
    def perform_action(cls, vehicle, action, state, dt_sec):
        """Perform throttle, break, and steering, keeping the previous steering angle as the start
        for the next steering angle.
        """
        throttle, brake, steering_change = action

                                                         
                                                          
                                                         
                 
        clipped_steering_change = np.clip(
            steering_change,
            -1,
            1,
        )

        p = 0.001                                                                 
        steering = np.clip(
            (1 - p) * state.last_steering_angle + clipped_steering_change * dt_sec,
            -1,
            1,
        )

        vehicle.control(
            throttle=np.clip(throttle, 0.0, 1.0),
            brake=np.clip(brake, 0.0, 1.0),
            steering=steering,
        )

        state.last_steering_angle = steering
