             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math
from itertools import cycle

import numpy as np
import pytest

from smarts.core.agent_interface import (
    ActionSpaceType,
    AgentInterface,
    NeighborhoodVehicles,
)
from smarts.core.coordinates import Heading
from smarts.core.plan import EndlessGoal, NavigationMission, Start
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.core.utils.custom_exceptions import RendererException


@pytest.fixture
def scenarios():
    mission = NavigationMission(
        start=Start(np.array((71.65, 63.78)), Heading(math.pi * 0.91)),
        goal=EndlessGoal(),
    )
    scenario = Scenario(
        scenario_root="scenarios/sumo/loop",
        traffic_specs=["scenarios/sumo/loop/build/traffic/basic.rou.xml"],
        missions={"Agent-007": mission},
    )
    return cycle([scenario])


@pytest.fixture
def smarts():
    buddha = AgentInterface(
        max_episode_steps=1000,
        neighborhood_vehicle_states=NeighborhoodVehicles(radius=20),
        action=ActionSpaceType.Lane,
    )
    agents = {"Agent-007": buddha}
    smarts = SMARTS(
        agents,
        traffic_sims=[SumoTrafficSimulation(headless=True)],
        envision=None,
    )

    yield smarts
    smarts.destroy()


def test_smarts_doesnt_leak_tasks_after_reset(smarts, scenarios):
    """We have had issues in the past where we would forget to clean up tasks between episodes
    resulting in a gradual decay in performance, this test gives us a bit of a smoke screen
    against this class of regressions.

    See #237 for details
    """
    try:
        num_tasks_before_reset = len(
            smarts.renderer._showbase_instance.taskMgr.mgr.getTasks()
        )
    except Exception as e:
        raise RendererException.required_to("test smarts_doesnt_leak_tasks_after_reset")

    scenario = next(scenarios)
    smarts.reset(scenario)

    for _ in range(10):
        smarts.step({})

    try:
        num_tasks_after_reset = len(
            smarts.renderer._showbase_instance.taskMgr.mgr.getTasks()
        )

    except Exception as e:
        raise RendererException.required_to("test smarts_doesnt_leak_tasks_after_reset")

    assert num_tasks_after_reset == num_tasks_before_reset
