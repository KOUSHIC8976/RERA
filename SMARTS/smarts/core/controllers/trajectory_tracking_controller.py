                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math
from typing import Sequence, Tuple

import numpy as np
from numpy.linalg import matrix_power

from smarts.core.utils.core_math import (
    lerp,
    low_pass_filter,
    min_angles_difference_signed,
    radians_to_vec,
    signed_dist_to_line,
)

METER_PER_SECOND_TO_KM_PER_HR = 3.6


class TrajectoryTrackingControllerState:
    """Controller state"""

    def __init__(self):
        self.heading_error_gain = None
        self.lateral_error_gain = None
        self.heading_error = 0
        self.lateral_error = 0
        self.velocity_error = 0
        self.integral_velocity_error = 0
        self.integral_windup_error = 0
        self.steering_state = 0
        self.throttle_state = 0


class TrajectoryTrackingController:
    """A trajectory tracking controller."""

    @staticmethod
    def perform_trajectory_tracking_MPC(
        trajectory: Tuple[
            Sequence[float], Sequence[float], Sequence[float], Sequence[float]
        ],
        vehicle,
        state,
        dt_sec: float,
        prediction_horizon: int = 5,
    ):
        """Attempts model predictive control for the given vehicle given an expected trajectory."""
        half_vehicle_len = vehicle.length / 2
        vehicle_mass, vehicle_inertia_z = vehicle.chassis.mass_and_inertia
        (
            heading_error,
            lateral_error,
        ) = TrajectoryTrackingController.calculate_heading_lateral_error(
            vehicle=vehicle,
            trajectory=trajectory,
            initial_look_ahead_distant=3,
            speed_reduction_activation=True,
        )

        raw_throttle = TrajectoryTrackingController.calculate_raw_throttle_feedback(
            vehicle=vehicle,
            state=state,
            trajectory=trajectory,
            velocity_gain=1,
            velocity_integral_gain=0,
            integral_velocity_error=0,
            velocity_damping_gain=0,
            windup_gain=0,
            traction_gain=8,
            speed_reduction_activation=True,
            throttle_filter_constant=10,
            dt_sec=dt_sec,
        )[0]
        if raw_throttle > 0:
            brake_norm, throttle_norm = 0, np.clip(raw_throttle, 0, 1)
        else:
            brake_norm, throttle_norm = np.clip(-raw_throttle, 0, 1), 0
        longitudinal_velocity = vehicle.chassis.longitudinal_lateral_speed[0]
                                                                            
                                                            
        longitudinal_velocity = max(0.1, longitudinal_velocity)

        state_matrix = np.array(
            [
                [0, 1, 0, 0],
                [
                    0,
                    -(
                        vehicle.chassis.front_rear_stiffness[0]
                        + vehicle.chassis.front_rear_stiffness[1]
                    )
                    / (vehicle_mass * longitudinal_velocity),
                    (
                        vehicle.chassis.front_rear_stiffness[0]
                        + vehicle.chassis.front_rear_stiffness[1]
                    )
                    / vehicle_mass,
                    half_vehicle_len
                    * (
                        vehicle.chassis.front_rear_stiffness[0]
                        + vehicle.chassis.front_rear_stiffness[1]
                    )
                    / (vehicle_mass * longitudinal_velocity),
                ],
                [0, 0, 0, 1],
                [
                    0,
                    half_vehicle_len
                    * (
                        -vehicle.chassis.front_rear_stiffness[0]
                        + vehicle.chassis.front_rear_stiffness[1]
                    )
                    / (vehicle_mass * longitudinal_velocity),
                    half_vehicle_len
                    * (
                        vehicle.chassis.front_rear_stiffness[0]
                        - vehicle.chassis.front_rear_stiffness[1]
                    )
                    / vehicle_mass,
                    (half_vehicle_len**2)
                    * (
                        vehicle.chassis.front_rear_stiffness[0]
                        - vehicle.chassis.front_rear_stiffness[1]
                    )
                    / (vehicle_mass * longitudinal_velocity),
                ],
            ]
        )
        input_matrix = np.array(
            [
                [0],
                [vehicle.chassis.front_rear_stiffness[0] / vehicle_mass],
                [0],
                [vehicle.chassis.front_rear_stiffness[1] / vehicle_inertia_z],
            ]
        )
        drift_matrix = TrajectoryTrackingController.mpc_drift_matrix(
            vehicle, trajectory, prediction_horizon
        )
        steering_norm = -TrajectoryTrackingController.MPC(
            trajectory,
            heading_error,
            lateral_error,
            dt_sec,
            state_matrix,
            input_matrix,
            drift_matrix,
            prediction_horizon,
        )

        vehicle.control(
            throttle=throttle_norm,
            brake=brake_norm,
            steering=steering_norm,
        )

                                                        
    @staticmethod
    def perform_trajectory_tracking_PD(
        trajectory,
        vehicle,
        state,
        dt_sec,
    ):
        """Attempts proportional derivative control for the vehicle given an expected
        trajectory.
        """
                                                        
        params = vehicle.chassis.controller_parameters
        final_heading_gain = params["final_heading_gain"]
        final_lateral_gain = params["final_lateral_gain"]
        final_steering_filter_constant = params["final_steering_filter_constant"]
        throttle_filter_constant = params["throttle_filter_constant"]
        velocity_gain = params["velocity_gain"]
        velocity_integral_gain = params["velocity_integral_gain"]
        traction_gain = params["traction_gain"]
        final_lateral_error_derivative_gain = params[
            "final_lateral_error_derivative_gain"
        ]
        final_heading_error_derivative_gain = params[
            "final_heading_error_derivative_gain"
        ]
        initial_look_ahead_distant = params["initial_look_ahead_distant"]
        derivative_activation = params["derivative_activation"]
        speed_reduction_activation = params["speed_reduction_activation"]
        velocity_damping_gain = params["velocity_damping_gain"]
        windup_gain = params["windup_gain"]

                                                                                                
                                                                                 
        lateral_gain = 0.61
        heading_gain = 0.01
        lateral_error_derivative_gain = 0.15
        heading_error_derivative_gain = 0.5

                                                                    
                                                                          
                                                                       
                                                                   
                                                                     
                                                      
        normalized_speed = np.clip(
            (METER_PER_SECOND_TO_KM_PER_HR * trajectory[3][0] - 20) / (80 - 20), 0, 1
        )
        adjust_gains_for_normalized_speed = False                                    
        if adjust_gains_for_normalized_speed:
            lateral_gain = lerp(3, final_lateral_gain, normalized_speed)
            lateral_error_derivative_gain = lerp(
                0.2, final_lateral_error_derivative_gain, normalized_speed
            )
            heading_gain = lerp(0.03, final_heading_gain, normalized_speed)
            heading_error_derivative_gain = lerp(
                1.5, final_heading_error_derivative_gain, normalized_speed
            )
            steering_filter_constant = lerp(
                12, final_steering_filter_constant, normalized_speed
            )
        elif vehicle.speed > 70 / METER_PER_SECOND_TO_KM_PER_HR:
            lateral_gain = 1.51
            heading_error_derivative_gain = 0.1

                                                                   
        steering_filter_constant = lerp(
            12, final_steering_filter_constant, normalized_speed
        )

        if abs(min_angles_difference_signed(trajectory[2][-1], trajectory[2][0])) > 2:
            throttle_filter_constant = 2.5

        if (
            abs(
                TrajectoryTrackingController.curvature_calculation(
                    trajectory, 0, num_points=3
                )
            )
            < 150
        ):
            heading_gain = 0.05
            lateral_error_derivative_gain = 0.015
            heading_error_derivative_gain = 0.05

        (
            heading_error,
            lateral_error,
        ) = TrajectoryTrackingController.calculate_heading_lateral_error(
            vehicle, trajectory, initial_look_ahead_distant, speed_reduction_activation
        )

        curvature_radius = TrajectoryTrackingController.curvature_calculation(
            trajectory
        )

                                                                                          
                                                                                               
        z_yaw = vehicle.chassis.velocity_vectors[1][2]
        derivative_term = (
            +heading_error_derivative_gain * z_yaw
            + lateral_error_derivative_gain
            * (lateral_error - state.lateral_error)
            / dt_sec
        )
                                                                                        
                                
                                                                                  
                                                                                 
                                                                                
                                     
        steering_feed_forward_term = 0.1 * (1 / curvature_radius) * (vehicle.speed) ** 2
        steering_raw = np.clip(
            derivative_activation * derivative_term
            + math.degrees(heading_gain * (heading_error))
            + 1 * lateral_gain * lateral_error
            - steering_feed_forward_term,
            -1,
            1,
        )
                                              
        state.steering_state = low_pass_filter(
            steering_raw, state.steering_state, steering_filter_constant, dt_sec
        )

        (
            raw_throttle,
            desired_speed,
        ) = TrajectoryTrackingController.calculate_raw_throttle_feedback(
            vehicle,
            state,
            trajectory,
            velocity_gain,
            velocity_integral_gain,
            state.integral_velocity_error,
            velocity_damping_gain,
            windup_gain,
            traction_gain,
            speed_reduction_activation,
            throttle_filter_constant,
            dt_sec,
        )

        if raw_throttle > 0:
            brake_norm, throttle_norm = 0, np.clip(raw_throttle, 0, 1)
        else:
            brake_norm, throttle_norm = np.clip(-raw_throttle, 0, 1), 0

        state.heading_error = heading_error
        state.lateral_error = lateral_error
        state.integral_velocity_error += (vehicle.speed - desired_speed) * dt_sec

        vehicle.control(
            throttle=throttle_norm,
            brake=brake_norm,
            steering=state.steering_state,
        )

    @staticmethod
    def calculate_raw_throttle_feedback(
        vehicle,
        state,
        trajectory,
        velocity_gain,
        velocity_integral_gain,
        integral_velocity_error,
        velocity_damping_gain,
        windup_gain,
        traction_gain,
        speed_reduction_activation,
        throttle_filter_constant,
        dt_sec,
    ):
        """Applies filters to the throttle for stability."""
        desired_speed = trajectory[3][-1]
                                                                                    
                                                                               
                                                                                       
                                                                                 
                                                                         
                                                                                   
                                                                           
                                                                                   
        absolute_ahead_curvature = abs(
            TrajectoryTrackingController.curvature_calculation(trajectory, 4)
        )
        if absolute_ahead_curvature < 30 and speed_reduction_activation:
            desired_speed = np.clip(0.8 * desired_speed, 0, 8.3)
        elif absolute_ahead_curvature < 100 and speed_reduction_activation:
            desired_speed *= 0.8

                                                                                   
                                                                                        
                                                                               
                                                                         
                                            
        velocity_error = vehicle.speed - desired_speed
        velocity_error_damping_term = (velocity_error - state.velocity_error) / dt_sec
        raw_throttle = METER_PER_SECOND_TO_KM_PER_HR * (
            -0.5 * velocity_gain * velocity_error
            - velocity_integral_gain
            * (integral_velocity_error + windup_gain * state.integral_windup_error)
            - velocity_damping_gain * velocity_error_damping_term
        )
        state.velocity_error = velocity_error
                                           
                                                                                                                                               
        state.integral_windup_error = np.clip(raw_throttle, -1, 1) - raw_throttle

                                                                        
                                                                   
        state.throttle_state = low_pass_filter(
            raw_throttle,
            state.throttle_state,
            throttle_filter_constant,
            dt_sec,
            raw_value=-traction_gain
            * abs(vehicle.chassis.longitudinal_lateral_speed[1]),
        )

        return (state.throttle_state, desired_speed)

    @staticmethod
    def calculate_heading_lateral_error(
        vehicle, trajectory, initial_look_ahead_distant, speed_reduction_activation
    ):
        """Determine vehicle heading error and lateral error in regards to the given trajectory."""
        heading_error = min_angles_difference_signed(
            (vehicle.heading % (2 * math.pi)), trajectory[2][0]
        )

                                                      
                           
                                                   
                                             
        look_ahead_points = initial_look_ahead_distant
                                                    
                                                                   
                                                                 
                           
        if (
            abs(TrajectoryTrackingController.curvature_calculation(trajectory, 4)) < 30
            and speed_reduction_activation
        ):
            initial_look_ahead_distant = 1
            look_ahead_points = 1

        path_vector = radians_to_vec(
            trajectory[2][min([look_ahead_points, len(trajectory[2]) - 1])]
        )

        vehicle_look_ahead_pt = [
            vehicle.position[0]
            - initial_look_ahead_distant * math.sin(vehicle.heading),
            vehicle.position[1]
            + initial_look_ahead_distant * math.cos(vehicle.heading),
        ]

        lateral_error = signed_dist_to_line(
            vehicle_look_ahead_pt,
            [
                trajectory[0][min([look_ahead_points, len(trajectory[0]) - 1])],
                trajectory[1][min([look_ahead_points, len(trajectory[1]) - 1])],
            ],
            path_vector,
        )
        return (heading_error, lateral_error)

    @staticmethod
    def curvature_calculation(trajectory, offset=0, num_points=5):
        """Attempts to approximate the curvature radius of a trajectory"""
        number_ahead_points = num_points
        relative_heading_sum, relative_distant_sum = 0, 0

        if len(trajectory[2]) <= number_ahead_points + offset:
            return 1e20

        for i in range(number_ahead_points):
            relative_heading_temp = min_angles_difference_signed(
                trajectory[2][i + 1 + offset], trajectory[2][i + offset]
            )
            relative_heading_sum += relative_heading_temp
            relative_distant_sum += abs(
                math.sqrt(
                    (trajectory[0][i + offset] - trajectory[0][i + offset + 1]) ** 2
                    + (trajectory[1][i + offset] - trajectory[1][i + offset + 1]) ** 2
                )
            )
                                                                
                                                                
                                     
        if relative_heading_sum == 0:
            return 1e20
        else:
            curvature_radius = relative_distant_sum / relative_heading_sum

        if curvature_radius == 0:
            curvature_radius == 1e-2
        return curvature_radius

    @staticmethod
    def mpc_drift_matrix(vehicle, trajectory, prediction_horizon=1):
        """TODO: Clarify"""
        half_vehicle_len = vehicle.length / 2
        vehicle_mass, vehicle_inertia_z = vehicle.chassis.mass_and_inertia
        factor_matrix = np.array(
            [
                [0],
                [
                    (
                        half_vehicle_len * vehicle.chassis.front_rear_stiffness[0]
                        + half_vehicle_len * vehicle.chassis.front_rear_stiffness[1]
                    )
                    / vehicle_mass
                    - (vehicle.chassis.longitudinal_lateral_speed[0]) ** 2
                ],
                [0],
                [
                    (
                        (half_vehicle_len**2)
                        * vehicle.chassis.front_rear_stiffness[0]
                        - (half_vehicle_len**2)
                        * vehicle.chassis.front_rear_stiffness[1]
                    )
                    / vehicle_inertia_z
                ],
            ]
        )
        matrix_drift = (
            TrajectoryTrackingController.curvature_calculation(trajectory) ** -1
        ) * factor_matrix
        for i in range(prediction_horizon - 1):
            matrix_drift = np.concatenate(
                (
                    matrix_drift,
                    (
                        TrajectoryTrackingController.curvature_calculation(
                            trajectory, i
                        )
                        ** -1
                    )
                    * factor_matrix,
                ),
                axis=1,
            )

        return matrix_drift

    @staticmethod
    def MPC(
        trajectory,
        heading_error,
        lateral_error,
        dt,
        state_matrix,
        input_matrix,
        drift_matrix,
        prediction_horizon=5,
    ):
        """Implementation of MPC, please see the following ref:
        Convex Optimization – Boyd and Vandenberghe
        https://github.com/markcannon/markcannon.github.io/blob/c3344814c9c79d5f0d5f3cf8fc2e7ef14cb4fad3/assets/downloads/teaching/C21_Model_Predictive_Control/mpc_notes.pdf
        https://markcannon.github.io/teaching/
        """
        matrix_A = np.eye(state_matrix.shape[0]) + dt * state_matrix
        matrix_B = dt * input_matrix
        matrix_B0 = dt * drift_matrix
        matrix_M = matrix_A
        matrix_C = np.concatenate(
            (
                matrix_B,
                np.zeros(
                    [matrix_B.shape[0], (prediction_horizon - 1) * matrix_B.shape[1]]
                ),
            ),
            axis=1,
        )

        matrix_T_tilde = matrix_B0[:, 0]

        for i in range(prediction_horizon - 1):
            matrix_M = np.concatenate((matrix_M, matrix_power(matrix_A, i + 2)), axis=0)
            matrix_T_tilde = np.concatenate(
                (
                    matrix_T_tilde,
                    np.matmul(
                        matrix_A,
                        matrix_T_tilde[
                            matrix_T_tilde.shape[0]
                            - matrix_B0.shape[0] : matrix_T_tilde.shape[0]
                        ],
                        matrix_B0[:, i + 1],
                    ),
                ),
                axis=0,
            )
            temp = np.matmul(matrix_power(matrix_A, i + 1), matrix_B)
            for j in range(i + 1, 0, -1):
                temp = np.concatenate(
                    (temp, np.matmul(matrix_power(matrix_A, j - 1), matrix_B)), axis=1
                )
            temp = np.concatenate(
                (
                    temp,
                    np.zeros(
                        [
                            matrix_B.shape[0],
                            (prediction_horizon - i - 2) * matrix_B.shape[1],
                        ]
                    ),
                ),
                axis=1,
            )
            matrix_C = np.concatenate((matrix_C, temp), axis=0)

                                                                      
                                                                               
                                                                              
                                                      
        Q_tilde = np.kron(np.eye(prediction_horizon), 0.1 * np.diag([354, 0, 14, 250]))
                                                    
        R_tilde = np.kron(np.eye(prediction_horizon), np.eye(1))
        matrix_H = (np.transpose(matrix_C)).dot(Q_tilde).dot(matrix_C) + R_tilde
        matrix_F = (np.transpose(matrix_C)).dot(Q_tilde).dot(matrix_M)

        matrix_F1 = (np.transpose(matrix_C)).dot(Q_tilde).dot(matrix_T_tilde)

                                                                        
                      
        unconstrained_optimal_solution = np.matmul(
            np.linalg.inv(2 * matrix_H),
            np.matmul(matrix_F, np.array([[lateral_error], [0], [heading_error], [0]]))
            + np.reshape(matrix_F1, (-1, 1)),
        )[0][0]

        return np.clip(-unconstrained_optimal_solution, -1, 1)
