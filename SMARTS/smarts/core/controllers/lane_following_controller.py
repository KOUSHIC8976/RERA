                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math

import numpy as np

from smarts.core.chassis import AckermannChassis
from smarts.core.controllers.trajectory_tracking_controller import (
    TrajectoryTrackingController,
)
from smarts.core.utils.core_math import (
    lerp,
    low_pass_filter,
    min_angles_difference_signed,
)

METER_PER_SECOND_TO_KM_PER_HR = 3.6


class LaneFollowingControllerState:
    """Controller state"""

                                                                               
                                      
    def __init__(self, target_lane_id):
        self.target_lane_id = target_lane_id
        self.target_speed = None
        self.heading_error_gain = None
        self.lateral_error_gain = None
        self.lateral_integral_error = 0
        self.integral_speed_error = 0
        self.steering_state = 0
        self.throttle_state = 0
        self.speed_error = 0
        self.min_curvature_location = (None, None)


class LaneFollowingController:
    """A controller that attempts to follow road waypoints along the vehicle's plan.

    Requires the controlled vehicle to have an Ackermann chassis.
    """

    lateral_error = -35
    heading_error = -15
    yaw_rate = -2
    side_slip_angle = -3

    @classmethod
    def perform_lane_following(
        cls,
        sim,
        agent_id: str,
        vehicle,
        controller_state: LaneFollowingControllerState,
        sensor_state,
        target_speed: float = 12.5,
        lane_change: int = 0,
    ):
        """Control a vehicle

        Args:
            sim:
                The simulator instance.
            agent_id:
                The id of the agent controlling the vehicle. XXX: unsure why this is needed
            vehicle:
                The vehicle that is to be controlled.
            controller_state:
                The previous controller state from this controller.
            sensor_state:
                The current sensor state from the vehicle's sensors.
            target_speed:
                The baseline target speed (controller may give more or less regardless.)
            lane_change:
                Lane index offset from vehicle's current lane.
        """
        assert isinstance(vehicle.chassis, AckermannChassis)
        state = controller_state
                                                                                    
                                                 
        wp_paths = sim.road_map.waypoint_paths(
            vehicle.pose, lookahead=16, route=sensor_state.get_plan(sim.road_map).route
        )
        assert wp_paths, "no waypoints found.  not near lane?"
        current_lane = LaneFollowingController.find_current_lane(
            wp_paths, vehicle.position
        )
        wp_path = wp_paths[np.clip(current_lane + lane_change, 0, len(wp_paths) - 1)]

                                                                          
                                                           
        ewma_road_curviness = 0.0
        for wp_a, wp_b in reversed(list(zip(wp_path, wp_path[1:]))):
            ewma_road_curviness = lerp(
                ewma_road_curviness,
                math.degrees(abs(wp_a.relative_heading(wp_b.heading))),
                0.03,
            )

        road_curviness_normalization = 2.5
        road_curviness = np.clip(
            ewma_road_curviness / road_curviness_normalization, 0, 1
        )
                                                                    
        num_trajectory_points = min([10, len(wp_path)])
        trajectory = [
            [wp_path[i].pos[0] for i in range(num_trajectory_points)],
            [wp_path[i].pos[1] for i in range(num_trajectory_points)],
            [wp_path[i].heading for i in range(num_trajectory_points)],
        ]
                                                                      
                                                                     
                                                                           
                                                           
        look_ahead_curvature = abs(
            TrajectoryTrackingController.curvature_calculation(trajectory, 4)
        )
                                                                  
                                                      
        min_curvature = 2
                                                                          
                                                                            
                        
        if look_ahead_curvature <= min_curvature:
            state.min_curvature_location = (
                wp_path[4].pos[0],
                wp_path[4].pos[1],
            )

                                  
                                                                  
                                                                   
                                   

                                                                  
                                                                      
                                                                       
                                                   
                                                             
        if road_curviness > 0.5:
            look_ahead_wp_num = 3
        else:
            look_ahead_wp_num = 4

        look_ahead_wp_num = min(look_ahead_wp_num, len(wp_path) - 1)

        reference_heading = wp_path[0].heading
        look_ahead_wp = wp_path[look_ahead_wp_num]
        look_ahead_dist = look_ahead_wp.dist_to(vehicle.position)
        vehicle_look_ahead_pt = [
            vehicle.position[0] - look_ahead_dist * math.sin(vehicle.heading),
            vehicle.position[1] + look_ahead_dist * math.cos(vehicle.heading),
        ]

                                                                                           
                              
                                                                    
                                                              
                                                           
        if road_curviness < 0.3:
            raw_throttle = (
                -METER_PER_SECOND_TO_KM_PER_HR * 1.8 * (vehicle.speed - target_speed)
            )
        elif road_curviness > 0.3 and road_curviness < 0.8:
            raw_throttle = (
                -0.6
                * METER_PER_SECOND_TO_KM_PER_HR
                * (vehicle.speed - np.clip(target_speed, 0, 6.94))
            )
        else:
            raw_throttle = (
                -0.6
                * METER_PER_SECOND_TO_KM_PER_HR
                * (vehicle.speed - np.clip(target_speed, 0, 5.56))
            )

        speed_error = vehicle.speed - target_speed
        state.integral_speed_error += speed_error * sim.last_dt
        velocity_error_damping_term = (speed_error - state.speed_error) / sim.last_dt
                                                                        
                                                                          
                                                                             
                                                                       
                                                                                 
                                                                              
                       
        lateral_force_coefficient = 1.5
        if vehicle.speed < 8 or target_speed < 6:
            lateral_force_coefficient = 0
                                                                   
                                                                   
        raw_throttle += (
            -0.2 * velocity_error_damping_term
            - 0.1 * state.integral_speed_error
            + abs(
                lateral_force_coefficient
                * math.sin(state.steering_state * vehicle.max_steering_wheel)
            )
        )
        state.speed_error = speed_error
                                                                     
                                                                        
                                                                   
                                      
        if (state.min_curvature_location != (None, None)) and math.sqrt(
            (vehicle.position[0] - state.min_curvature_location[0]) ** 2
            + (vehicle.position[1] - state.min_curvature_location[1]) ** 2
        ) < 2:
            reference_heading = wp_path[look_ahead_wp_num].heading

                                                           
                                                                      
                                                                        
                                                    
                                                                   
        desired_poles = np.array(
            [
                cls.lateral_error,
                cls.heading_error,
                cls.yaw_rate,
                cls.side_slip_angle,
            ]
        )

        LaneFollowingController.calculate_lateral_gains(
            sim, state, vehicle, desired_poles, target_speed
        )
                               
        controller_lat_error = wp_path[look_ahead_wp_num].signed_lateral_error(
            vehicle_look_ahead_pt
        )

        curvature_radius = TrajectoryTrackingController.curvature_calculation(
            trajectory
        )
        brake_norm = 0
        if raw_throttle < 0:
            brake_norm = np.clip(-raw_throttle, 0, 1)
            throttle_norm = 0
        else:
                                                                       
                                                                           
                                                                          
                                                                      
                               
            if vehicle.speed > 70 / 3.6 and abs(curvature_radius) <= 1e3:
                traction_gain = 4.5
            elif 40 / 3.6 <= vehicle.speed <= 70 / 3.6 and abs(curvature_radius) <= 3:
                traction_gain = 2.5
            else:
                traction_gain = 0.5

            throttle_norm = np.clip(
                raw_throttle
                - traction_gain
                * METER_PER_SECOND_TO_KM_PER_HR
                * abs(vehicle.chassis.longitudinal_lateral_speed[1]),
                0,
                1,
            )
                                                                 
                                                                       
                                                                   
                                                                      
                                                                   
                                                                      
                                             
        state.lateral_integral_error += sim.last_dt * controller_lat_error
                                                                  
                                                                  
                                                               
                                                                 
                                                        
                                                                            
        steering_feed_forward_gain = 0.15

        if abs(curvature_radius) < 7:
            steering_feed_forward_gain = 0.45

        steering_controller_feed_forward = (
            1
            * steering_feed_forward_gain
            * (1 / curvature_radius)
            * (vehicle.speed) ** 2
        )
        normalized_speed = np.clip(vehicle.speed * 3.6 / 100, 0, 1)
        heading_speed_gain = -lerp(0.5, 14, normalized_speed)
        yaw_rate_speed_gain = lerp(5.75, 11.75, normalized_speed)
        lateral_speed_gain = np.clip(lerp(-1, 14, normalized_speed), 1, 2)

        max_steering_nomralized = 1
        if abs(curvature_radius) > 1e7 and lane_change != 0:
            heading_speed_gain = -4.95
            yaw_rate_speed_gain = 1
            lateral_speed_gain = 0.22
            max_steering_nomralized = 0.12

        z_yaw = vehicle.chassis.velocity_vectors[1][2]
        heading_error = min_angles_difference_signed(
            (vehicle.heading % (2 * math.pi)), reference_heading
        )
        steering_norm = np.clip(
            -heading_speed_gain * math.degrees(state.heading_error_gain) * heading_error
            + lateral_speed_gain * state.lateral_error_gain * (controller_lat_error)
            + yaw_rate_speed_gain * z_yaw
            + 0.3 * state.lateral_integral_error
            - steering_controller_feed_forward,
            -max_steering_nomralized,
            max_steering_nomralized,
        )
                                                                  
                                             
        steering_filter_constant = 5.5

        state.steering_state = low_pass_filter(
            steering_norm,
            state.steering_state,
            steering_filter_constant,
            sim.last_dt,
        )

                                                                
                                             
                                              
        throttle_filter_constant = 2

        state.throttle_state = low_pass_filter(
            throttle_norm,
            state.throttle_state,
            throttle_filter_constant,
            sim.last_dt,
            lower_bound=0,
        )
                                                 
        vehicle.control(
            throttle=state.throttle_state,
            brake=brake_norm,
            steering=state.steering_state,
        )

        LaneFollowingController._update_target_lane_if_reached_end_of_lane(
            agent_id,
            vehicle,
            controller_state,
            sensor_state.get_plan(sim.road_map),
        )

    @staticmethod
    def find_current_lane(wp_paths, vehicle_position):
        """Find the lane of the vehicle given a set of waypoint paths."""
        relative_distant_lane = [
            np.linalg.norm(np.subtract(wp_paths[idx][0].pos, vehicle_position[:2]))
            for idx in range(len(wp_paths))
        ]
        return np.argmin(relative_distant_lane)

    @staticmethod
    def place_poles(A: np.ndarray, B: np.ndarray, poles: np.ndarray) -> np.ndarray:
        """Given a linear system described by ẋ = Ax + Bu, compute the gain matrix K
        such that the closed loop eigenvalues of A - BK are in the desired pole locations.

        References:
         - https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.place_poles.html
         - https://en.wikipedia.org/wiki/Ackermann%27s_formula
        """

                                
        C = np.hstack(
            [B] + [np.linalg.matrix_power(A, i) @ B for i in range(1, A.shape[0])]
        )

                                                     
        poly = np.real(np.poly(poles))

                                         
        n = np.size(poly)
        p = poly[n - 1] * np.linalg.matrix_power(A, 0)
        for i in np.arange(1, n):
            p = p + poly[n - i - 1] * np.linalg.matrix_power(A, i)
        return np.linalg.solve(C, p)[-1][:]

    @staticmethod
    def calculate_lateral_gains(sim, state, vehicle, desired_poles, target_speed):
        """Update the state lateral gains"""
                                                              
                                                     
        if state.target_speed == target_speed:
            return

        state.target_speed = target_speed

                        
        half_vehicle_len = vehicle.length / 2
        vehicle_mass, vehicle_inertia_z = vehicle.chassis.mass_and_inertia
        road_stiffness = sim.road_stiffness

                                           
        if target_speed > 0:
            state_matrix = np.array(
                [
                    [0, target_speed, 0, target_speed],
                    [0, 0, 1, 0],
                    [
                        0,
                        0,
                        -(2 * road_stiffness * (half_vehicle_len**2))
                        / (target_speed * vehicle_inertia_z),
                        0,
                    ],
                    [
                        0,
                        0,
                        -1,
                        -2 * road_stiffness / (vehicle_mass * target_speed),
                    ],
                ]
            )
            input_matrix = np.array(
                [
                    [0],
                    [0],
                    [half_vehicle_len * road_stiffness / vehicle_inertia_z],
                    [road_stiffness / (vehicle_mass * target_speed)],
                ]
            )
            K = LaneFollowingController.place_poles(
                state_matrix, input_matrix, desired_poles
            )

                                                                                    
                                                                                   
                                                                                      
            state.lateral_error_gain = np.clip(K[0], 3.4, 4.1)
            state.heading_error_gain = np.clip(K[1], 0.02, 0.04)
        else:
                                                                            
                                                                             
                                               
            state.heading_error_gain = 0.01
            state.lateral_error_gain = 0.36

    @staticmethod
    def _update_target_lane_if_reached_end_of_lane(
        agent_id, vehicle, controller_state, plan
    ):
                                                                        
                                              
        state = controller_state
        lane = plan.road_map.lane_by_id(state.target_lane_id)
        paths = lane.waypoint_paths_for_pose(
            vehicle.pose, lookahead=2, route=plan.route
        )

        candidate_next_wps = []
        for path in paths:
            wps_of_next_lanes_on_path = [
                wp for wp in path if wp.lane_id != state.target_lane_id
            ]

            if wps_of_next_lanes_on_path == []:
                continue

            next_wp = wps_of_next_lanes_on_path[0]
            candidate_next_wps.append(next_wp)

        if candidate_next_wps == []:
            return

        next_wp = min(
            candidate_next_wps,
            key=lambda wp: abs(wp.signed_lateral_error(vehicle.position))
            + abs(wp.relative_heading(vehicle.heading)),
        )

        state.target_lane_id = next_wp.lane_id
