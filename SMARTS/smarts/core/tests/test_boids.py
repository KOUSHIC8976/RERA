             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import os
import re
from collections import defaultdict
from dataclasses import dataclass

import pytest
from helpers.bubbles import bubble_geometry
from helpers.scenario import temp_scenario
from shapely.geometry import Point

import smarts.sstudio.sstypes as t
from smarts.core import seed
from smarts.core.local_traffic_provider import LocalTrafficProvider
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.sstudio import gen_scenario


@pytest.fixture
def bubble():
    return t.Bubble(
        zone=t.PositionalZone(pos=(100, 0), size=(20, 20)),
        margin=10,
        actor=t.BoidAgentActor(
                                                                                       
            name="hive-mind",
            agent_locator="scenarios.sumo.straight.3lane_bubble.agent_prefabs:pose-boid-agent-v0",
        ),
    )


@pytest.fixture(params=["SUMO", "SMARTS"])
def traffic_sim(request):
    return getattr(request, "param", "SUMO")


@pytest.fixture
def scenarios(bubble, traffic_sim):
    with temp_scenario(name="straight", map="maps/straight.net.xml") as scenario_root:
        traffic = t.Traffic(
            engine=traffic_sim,
            flows=[
                t.Flow(
                    route=t.Route(
                        begin=("west", lane_idx, 0),
                        end=("east", lane_idx, "max"),
                    ),
                    rate=50,
                    actors={
                        t.TrafficActor("car"): 1,
                    },
                )
                for lane_idx in range(3)
            ],
        )

        gen_scenario(
            t.Scenario(traffic={"all": traffic}, bubbles=[bubble]),
            output_dir=scenario_root,
        )

        yield Scenario.variations_for_all_scenario_roots([str(scenario_root)], [])


@pytest.fixture
def smarts(traffic_sim):
    traffic_sims = (
        [LocalTrafficProvider()]
        if traffic_sim == "SMARTS"
        else [SumoTrafficSimulation()]
    )
    smarts = SMARTS({}, traffic_sims=traffic_sims)
    yield smarts
    smarts.destroy()


@dataclass
class ZoneSteps:
    in_bubble: int = 0
    outside_bubble: int = 0
    airlock_entry: int = 0
    airlock_exit: int = 0


                                                                 
@pytest.mark.parametrize("traffic_sim", ["SUMO", "SMARTS"], indirect=True)
def test_boids(smarts, scenarios, bubble):
                                                                   
    seed(int(os.getenv("PYTHONHASHSEED", 42)))

    scenario = next(scenarios)
    smarts.reset(scenario)

    index = smarts.vehicle_index
    geometry = bubble_geometry(bubble, smarts.road_map)

    triggered_multiple_vehicles_in_bubble = False
    triggered_multiple_vehicles_airlocked = False

                             
    steps_driven_in_zones = defaultdict(lambda: ZoneSteps())
                                                                                     
                                                                                     
                 
    for _ in range(500):
        smarts.step({})

        hijacked_actor_ids = []
        shadowed_actor_ids = []

        for vehicle in index.vehicles:
            position = Point(vehicle.position)
            in_bubble = position.within(geometry.bubble)
            is_shadowing = index.shadower_id_from_vehicle_id(vehicle.id) is not None
            is_agent_controlled = vehicle.id in index.agent_vehicle_ids()

            vehicle_id = (
                vehicle.id
                if traffic_sim == "SUMO"
                else re.sub(r"_\d+$", "", vehicle.id)
            )
            zone_steps = steps_driven_in_zones[vehicle_id]
            if position.within(geometry.bubble):
                zone_steps.in_bubble += 1
                hijacked_actor_ids.append(index.owner_id_from_vehicle_id(vehicle.id))
                assert in_bubble and not is_shadowing and is_agent_controlled
            elif position.within(geometry.airlock_entry):
                zone_steps.airlock_entry += 1
                shadowed_actor_ids.append(index.shadower_id_from_vehicle_id(vehicle.id))
                assert not in_bubble and is_shadowing and not is_agent_controlled
            elif position.within(geometry.airlock_exit):
                zone_steps.airlock_exit += 1
                                                                                    
                assert not in_bubble and not is_shadowing and is_agent_controlled
            else:
                zone_steps.outside_bubble += 1
                assert not in_bubble and not is_shadowing and not is_agent_controlled

        if len(hijacked_actor_ids) > 1:
            triggered_multiple_vehicles_in_bubble = True

        if len(shadowed_actor_ids) > 1:
            triggered_multiple_vehicles_airlocked = True

        assert (
            len(set(hijacked_actor_ids)) <= 1
        ), "Boid vehicles must be controlled by the same actor"
        assert (
            len(set(shadowed_actor_ids)) <= 1
        ), "Boid vehicles must be shadowed by the same actor"

                                                                              
    min_steps = 5
    for vehicle_id, zone in steps_driven_in_zones.items():
        assert all(
            [
                zone.in_bubble > min_steps,
                zone.outside_bubble > min_steps,
                zone.airlock_entry > min_steps,
                zone.airlock_exit > min_steps,
            ]
        ), (
            f"vehicle_id={vehicle_id}, zone={zone} doesn't meet "
            f"min_steps={min_steps} requirement"
        )

    assert (
        triggered_multiple_vehicles_in_bubble
    ), "Multiple vehicles did not enter the bubble simultaneously"
    assert (
        triggered_multiple_vehicles_airlocked
    ), "Multiple vehicles were not airlocked simultaneously"
