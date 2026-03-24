             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import logging
import math
from typing import Dict

import gymnasium as gym
import numpy as np
import pytest
from panda3d.core import OrthographicLens, Point2, Point3

from smarts.core.agent import Agent
from smarts.core.agent_interface import (
    OGM,
    RGB,
    AgentInterface,
    DrivableAreaGridMap,
    NeighborhoodVehicles,
    OcclusionMap,
    RoadWaypoints,
    Signals,
)
from smarts.core.colors import SceneColors
from smarts.core.controllers import ActionSpaceType
from smarts.core.coordinates import Heading, Point
from smarts.core.observations import DrivableAreaGridMap as ObsDrivableAreaGridMap
from smarts.core.observations import GridMapMetadata, Observation, TopDownRGB
from smarts.core.plan import (
    NavigationMission,
    PositionalGoal,
    Start,
    default_entry_tactic,
)
from smarts.core.scenario import Scenario
from smarts.core.signals import SignalLightState
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.env.utils.observation_conversion import ObservationOptions
from smarts.zoo.agent_spec import AgentSpec

logging.basicConfig(level=logging.INFO)

AGENT_ID = "Agent-007"

NUM_STEPS = 20
MAP_WIDTH = 1536
MAP_HEIGHT = 1536
HALF_WIDTH = MAP_WIDTH / 2
HALF_HEIGHT = MAP_HEIGHT / 2
MAP_RESOLUTION = 50 / 256
SAMPLE_RANGE = 10

ROAD_COLOR = np.array(SceneColors.Road.value[0:3]) * 255


@pytest.fixture
def agent_interface():
    return AgentInterface(
        road_waypoints=RoadWaypoints(40),
        neighborhood_vehicle_states=NeighborhoodVehicles(
            radius=max(MAP_WIDTH * MAP_RESOLUTION, MAP_HEIGHT * MAP_RESOLUTION) * 0.5
        ),
        drivable_area_grid_map=DrivableAreaGridMap(
            width=MAP_WIDTH, height=MAP_HEIGHT, resolution=MAP_RESOLUTION
        ),
        occupancy_grid_map=OGM(
            width=MAP_WIDTH, height=MAP_HEIGHT, resolution=MAP_RESOLUTION
        ),
        occlusion_map=OcclusionMap(
            width=MAP_WIDTH, height=MAP_HEIGHT, resolution=MAP_RESOLUTION
        ),
        top_down_rgb=RGB(width=MAP_WIDTH, height=MAP_HEIGHT, resolution=MAP_RESOLUTION),
        action=ActionSpaceType.Lane,
        signals=Signals(100.0),
    )


@pytest.fixture
def agent_spec(agent_interface):
    return AgentSpec(
        interface=agent_interface,
        agent_builder=lambda: Agent.from_function(lambda _: 0),
    )


@pytest.fixture
def env(agent_spec: AgentSpec):
    _env = gym.make(
        "smarts.env:hiway-v1",
        scenarios=["scenarios/sumo/figure_eight"],
        agent_interfaces={AGENT_ID: agent_spec.interface},
        headless=True,
        fixed_timestep_sec=0.1,
        seed=42,
        observation_options=ObservationOptions.unformatted,
    )

    yield _env
    _env.close()


def project_2d(lens, img_metadata: GridMapMetadata, pos):
    center = np.array(img_metadata.camera_position)
    heading = img_metadata.camera_heading

                                              
    p_translated = pos - center

                                                                                                   
    p_rotated = np.array(
        [
            p_translated[0] * np.cos(-heading) - p_translated[1] * np.sin(-heading),
            p_translated[0] * np.sin(-heading) + p_translated[1] * np.cos(-heading),
            p_translated[2],
        ]
    )

    v_2d_pos_normalized = Point2()
    v_3d_pos = Point3(
        p_rotated[0], p_rotated[2], p_rotated[1]
    )                                                

    x = int(HALF_HEIGHT)
    y = int(HALF_WIDTH)

                                                                            
    if lens.project(v_3d_pos, v_2d_pos_normalized):

                                                                                                        
                                                                                                  
                                                                                            
        x = int(-v_2d_pos_normalized[1] * HALF_HEIGHT + HALF_HEIGHT)
        y = int(v_2d_pos_normalized[0] * HALF_WIDTH + HALF_WIDTH)

    return x, y


def apply_tolerance(arr, x, y, tolerance):
    return arr[x - tolerance : x + tolerance, y - tolerance : y + tolerance, :]


def sample_vehicle_pos(
    lens,
    rgb: TopDownRGB,
    drivable_area: ObsDrivableAreaGridMap,
    vehicle_pos,
):
    rgb_x, rgb_y = project_2d(lens, rgb.metadata, vehicle_pos)
                                                                
    drivable_area_x, drivable_area_y = project_2d(
        lens, drivable_area.metadata, vehicle_pos
    )

                                                             
         
    tolerance = 2
    assert np.count_nonzero(rgb.data[rgb_x, rgb_y, :]) and np.count_nonzero(
        apply_tolerance(rgb.data, rgb_x, rgb_y, tolerance) != ROAD_COLOR
    )

         
                                                                                 
                                                                                 

                                                
                            
    assert np.count_nonzero(
        apply_tolerance(drivable_area.data, drivable_area_x, drivable_area_y, tolerance)
    )


def test_observations(env, agent_spec):
    agent = agent_spec.build_agent()
    observations: Dict[str, Observation] = env.reset()[0]

                                    
    for _ in range(NUM_STEPS):
        agent_obs = observations[AGENT_ID]
        agent_action = agent.act(agent_obs)
        observations, _, _, _, _ = env.step({AGENT_ID: agent_action})

         
    rgb = observations[AGENT_ID].top_down_rgb

         
    occ = observations[AGENT_ID].occlusion_map

                   
    drivable_area = observations[AGENT_ID].drivable_area_grid_map

    lens = OrthographicLens()
    lens.setFilmSize(MAP_RESOLUTION * MAP_WIDTH, MAP_RESOLUTION * MAP_HEIGHT)

                           
    ego_vehicle_position = observations[AGENT_ID].ego_vehicle_state.position
    sample_vehicle_pos(
        lens,
        rgb,
        drivable_area,
        ego_vehicle_position,
    )

                                 
    for neighbor_vehicle in observations[AGENT_ID].neighborhood_vehicle_states:
        sample_vehicle_pos(
            lens,
            rgb,
            drivable_area,
            neighbor_vehicle.position,
        )

                     
    for paths in observations[AGENT_ID].road_waypoints.lanes.values():
        for path in paths:
            first_wp = path[0]
            last_wp = path[-1]

            first_wp_pos = np.array([first_wp.pos[0], first_wp.pos[1], 0])
            last_wp_pos = np.array([last_wp.pos[0], last_wp.pos[1], 0])

            rgb_first_wp_x, rgb_first_wp_y = project_2d(
                lens, rgb.metadata, first_wp_pos
            )
            rgb_last_wp_x, rgb_last_wp_y = project_2d(lens, rgb.metadata, last_wp_pos)

            drivable_area_first_wp_x, drivable_area_first_wp_y = project_2d(
                lens, drivable_area.metadata, first_wp_pos
            )
            drivable_area_last_wp_x, drivable_area_last_wp_y = project_2d(
                lens, drivable_area.metadata, last_wp_pos
            )

                                                                                     
                 
            assert np.count_nonzero(rgb.data[rgb_first_wp_x, rgb_first_wp_y, :])
            assert np.count_nonzero(rgb.data[rgb_last_wp_x, rgb_last_wp_y, :])

                                    
            assert np.count_nonzero(
                drivable_area.data[
                    drivable_area_first_wp_x, drivable_area_first_wp_y, :
                ]
            )
            assert np.count_nonzero(
                drivable_area.data[drivable_area_last_wp_x, drivable_area_last_wp_y, :]
            )

    assert len(observations[AGENT_ID].signals) == 0


@pytest.fixture
def scenario():
    mission = NavigationMission(
        start=Start(np.array((20.40, 68.40)), Heading(-0.5 * math.pi)),
        goal=PositionalGoal(Point(128.40, 0), 10),
        entry_tactic=default_entry_tactic(1.0),
    )
    return Scenario(
        scenario_root="scenarios/sumo/intersections/2lane",
        traffic_specs=[
            "scenarios/sumo/intersections/2lane/build/traffic/vertical.rou.xml"
        ],
        missions={AGENT_ID: mission},
    )


@pytest.fixture
def smarts(agent_interface):
    ai = agent_interface
    ai.action = ActionSpaceType.LaneWithContinuousSpeed
    smarts = SMARTS(
        {AGENT_ID: ai},
        traffic_sims=[SumoTrafficSimulation(headless=True)],
        envision=None,
    )
    yield smarts
    smarts.destroy()


def test_signal_observations(smarts, scenario):
    observations: Dict[str, Observation] = smarts.reset(scenario)

                                             
    agent = Agent.from_function(lambda _: (1.0, 0))

                                    
    for step in range(900):
        agent_obs = observations[AGENT_ID]
        agent_action = agent.act(agent_obs)
        observations, _, dones, _ = smarts.step({AGENT_ID: agent_action})
        if dones[AGENT_ID]:
            break
        my_obs = observations[AGENT_ID]
        signals = my_obs.signals
        pos = my_obs.ego_vehicle_state.position
        if step < 2:
                                  
            assert len(signals) == 0, f"step={step}, pos={pos}"
        else:
            assert len(signals) == 1, f"step={step}, pos={pos}"
            assert (
                signals[0].controlled_lanes[0] == ":junction-intersection_9_0"
            ), f"step={step}"
            assert len(signals[0].controlled_lanes) == 1, f"step={step}"
            if step < 448:
                assert signals[0].state == SignalLightState.STOP, f"{step}"
                assert signals[0].last_changed is None, f"{step}"
            elif step < 798:
                assert signals[0].state == SignalLightState.GO, f"{step}"
                assert np.isclose(signals[0].last_changed, 45.1), f"{step}"
            elif step < 898:
                assert signals[0].state == SignalLightState.CAUTION, f"{step}"
                assert np.isclose(signals[0].last_changed, 80.1), f"{step}"
            else:
                assert signals[0].state == SignalLightState.STOP, f"{step}"
                assert np.isclose(signals[0].last_changed, 90.1), f"{step}"
