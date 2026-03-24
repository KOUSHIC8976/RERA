                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
                                                              

import heapq

import numpy as np

from smarts.core.agent_interface import AgentInterface
from smarts.core.controllers import ActionSpaceType


def observation_adapter(env_obs):
    ego_feature_num = 4
    npc_feature_num = 5
    near_npc_number = 5
    mask_size = near_npc_number + 1
    env_state_size = ego_feature_num + near_npc_number * npc_feature_num
                   
    ego_states = env_obs.ego_vehicle_state
    ego_x = ego_states.position[0]
    ego_y = ego_states.position[1]
    ego_loc = ego_states.position[0:2]
    ego_mission = ego_states.mission
    ego_yaw = ego_states.heading
    ego_speed = ego_states.speed
                                  
    detect_range = 37.5
    veh_within_detect_range_list = []
    for index, vehicle_state in enumerate(env_obs.neighborhood_vehicle_states):
        npc_loc = vehicle_state.position[0:2]
        distance = np.linalg.norm(npc_loc - ego_loc)
        if distance < detect_range:
            add_dict = {"vehicle_state": vehicle_state, "distance": distance}
            veh_within_detect_range_list.append(add_dict)

    r_veh_list = []
    ir_veh_list = []
                              
    for veh_dic in veh_within_detect_range_list:
        npc_x = veh_dic["vehicle_state"].position[0]
        npc_y = veh_dic["vehicle_state"].position[1]
        npc_yaw = veh_dic["vehicle_state"].heading

        distance = veh_dic["distance"]
        y_relative = (npc_y - ego_y) * np.cos(ego_yaw) - (npc_x - ego_x) * np.sin(
            ego_yaw
        )

        yaw_relative = npc_yaw - ego_yaw

        if y_relative < -5 or (yaw_relative < 0.1 and distance > 10):
            ir_veh_list.append(veh_dic)
        else:
            r_veh_list.append(veh_dic)

                                                   
    _near_npc = heapq.nsmallest(
        near_npc_number, r_veh_list, key=lambda s: s["distance"]
    )
    distance_list = []
    for i in range(len(_near_npc)):
        distance_list.append(_near_npc[i]["distance"])
                                          
    r_npc_list = [x["vehicle_state"] for x in _near_npc]
    ir_npc_list = [x["vehicle_state"] for x in ir_veh_list]

                           
    env_state = []
    if ego_states.edge_id == "edge-south-SN":              
        ego_pos_flag = [1, 0, 0]
    elif "junction" in ego_states.edge_id:            
        ego_pos_flag = [0, 1, 0]
    else:             
        ego_pos_flag = [0, 0, 1]

    ego_state = ego_pos_flag + [ego_speed]
                             
    env_state += ego_state
                   
    for veh_state in r_npc_list:
                                     
        npc_x = veh_state.position[0]
        npc_y = veh_state.position[1]
        npc_yaw = veh_state.heading
        x_relative = (npc_y - ego_y) * np.sin(ego_yaw) + (npc_x - ego_x) * np.cos(
            ego_yaw
        )
        y_relative = (npc_y - ego_y) * np.cos(ego_yaw) - (npc_x - ego_x) * np.sin(
            ego_yaw
        )
                             
        delta_yaw = npc_yaw - ego_yaw
               
        npc_speed = veh_state.speed
                                     
                                                                   
        npc_state = [
            x_relative,
            y_relative,
            npc_speed,
            np.cos(delta_yaw),
            np.sin(delta_yaw),
        ]
                                                                   

                           
        env_state += npc_state

                                                              
    mask = list(np.ones(mask_size))
    if len(env_state) < env_state_size:
        zero_padding_num = int((env_state_size - len(env_state)) / npc_feature_num)
        for _ in range(zero_padding_num):
            mask.pop()
        for _ in range(zero_padding_num):
            mask.append(0)
        while len(env_state) < env_state_size:
            env_state.append(0)

    goal_x = ego_mission.goal.position[0]
    if goal_x == 127.6:
        task = [1, 0, 0, 1]
    elif goal_x == 151.6:
        task = [0, 1, 0, 1]
    elif goal_x == 172.4:
        task = [0, 0, 1, 1]
    aux_state = mask + task

                      
    total_state = np.array(env_state + aux_state, dtype=np.float32)
                                         
    return total_state


def action_adapter(action):
    target_speed = np.clip(action[0] - action[1] / 4, 0, 1)
    target_speed = target_speed * 12

    agent_action = [target_speed, int(0)]
    return agent_action


def reward_adapter(env_obs, reward):
                     
    goal_x = env_obs.ego_vehicle_state.mission.goal.position[0]
    if goal_x == 127.6:
        task = [1, 0, 0, 1]
    elif goal_x == 151.6:
        task = [0, 1, 0, 1]
    elif goal_x == 172.4:
        task = [0, 0, 1, 1]

                           
    reward_c = 0.0
    reward_s = 0.0
    ego_events = env_obs.events

              
    collision = len(ego_events.collisions) > 0                   
    time_exceed = ego_events.reached_max_episode_steps                      
    reach_goal = ego_events.reached_goal
             
    reward_c += -0.3             
    if collision:
        print("collision:", ego_events.collisions)
        print("nearest veh:", observation_adapter(env_obs)[4:9])
        print("Failure. Ego vehicle collides with npc vehicle.")
        reward_s += -650
    elif time_exceed:
        print("nearest veh:", observation_adapter(env_obs)[4:9])
        print("Failure. Time exceed.")
        reward_c += -50
            
    else:
        if reach_goal:
            print("nearest veh:", observation_adapter(env_obs)[4:9])
            print("Success. Ego vehicle reached goal.")
            reward_s += 30

                                  
    reward = [i * reward_s for i in task[0:3]] + [reward_c]

    return reward


def get_aux_info(env_obs):
    ego_events = env_obs.events
    collision = len(ego_events.collisions) > 0                   
    time_exceed = ego_events.reached_max_episode_steps                      
    reach_goal = ego_events.reached_goal
    if collision:
        aux_info = "collision"
    elif time_exceed:
        aux_info = "time_exceed"
    elif reach_goal:
        aux_info = "success"
    else:
        aux_info = "running"
    return aux_info


cross_interface = AgentInterface(
    max_episode_steps=500,
    neighborhood_vehicle_states=True,
    waypoint_paths=True,
    action=ActionSpaceType.LaneWithContinuousSpeed,
)
