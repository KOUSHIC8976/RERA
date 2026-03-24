             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import time

import pytest
from helpers.scenario import temp_scenario

from smarts.core.agent_interface import ActionSpaceType, AgentInterface
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.sstudio import gen_scenario
from smarts.sstudio import sstypes as t

AGENT_1 = "Agent_007"


@pytest.fixture
def scenarios():
    with temp_scenario(name="6lane", map="maps/6lane.net.xml") as scenario_root:

        def actor_gen(id_):
            return [
                t.SocialAgentActor(
                    name=f"non-interactive-agent-{speed}-v0_{id_}",
                    agent_locator="zoo.policies:non-interactive-agent-v0",
                    policy_kwargs={"speed": speed},
                )
                for speed in [10, 30, 80]
            ]

        def to_mission(start_edge, end_edge):
            route = t.Route(begin=(start_edge, 1, 0), end=(end_edge, 1, "max"))
            return t.Mission(route=route)

        def fifth_mission(start_edge, end_edge):
            route = t.Route(begin=(start_edge, 0, 0), end=(end_edge, 0, "max"))
            return t.Mission(route=route)

        gen_scenario(
            t.Scenario(
                social_agent_missions={
                    "group-1": (
                        actor_gen(1),
                        [to_mission("edge-north-NS", "edge-south-NS")],
                    ),
                    "group-2": (
                        actor_gen(2),
                        [to_mission("edge-west-WE", "edge-east-WE")],
                    ),
                    "group-3": (
                        actor_gen(3),
                        [to_mission("edge-east-EW", "edge-west-EW")],
                    ),
                    "group-4": (
                        actor_gen(4),
                        [to_mission("edge-south-SN", "edge-north-SN")],
                    ),
                    "group-5": (
                        actor_gen(5),
                        [fifth_mission("edge-south-SN", "edge-east-WE")],
                    ),
                },
                ego_missions=[
                    t.Mission(
                        t.Route(
                            begin=("edge-west-WE", 0, 0), end=("edge-east-WE", 0, "max")
                        )
                    )
                ],
            ),
            output_dir=scenario_root,
        )
        yield Scenario.variations_for_all_scenario_roots(
            [str(scenario_root)], [AGENT_1]
        )


@pytest.fixture
def smarts():
    laner = AgentInterface(
        max_episode_steps=1000,
        action=ActionSpaceType.Lane,
    )

    agents = {AGENT_1: laner}
    smarts = SMARTS(
        agents,
        traffic_sims=[SumoTrafficSimulation(headless=True)],
        envision=None,
    )

    yield smarts
    smarts.destroy()


def test_smarts_framerate(smarts, scenarios):
    scenario = next(scenarios)
    smarts.reset(scenario)

    for _ in range(10):
        step_start_time = int(time.time() * 1000)
        smarts.step({AGENT_1: "keep_lane"})
        step_end_time = int(time.time() * 1000)
        delta = step_end_time - step_start_time
        step_fps = round(1000 / delta, 2)
        assert step_fps >= 2
