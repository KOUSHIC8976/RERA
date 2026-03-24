             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from unittest import mock

import pytest

from smarts.core.actor import ActorState
from smarts.core.agent_interface import (
    AgentInterface,
    AgentsAliveDoneCriteria,
    AgentsListAlive,
    DoneCriteria,
    InterestDoneCriteria,
)
from smarts.core.scenario import Scenario
from smarts.core.sensors import Sensors
from smarts.core.smarts import SMARTS, SimulationFrame
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation

AGENT1 = "agent1"
AGENT2 = "agent2"
AGENT3 = "agent3"


@pytest.fixture
def scenario():
    scenario = Scenario(
        scenario_root="scenarios/sumo/loop",
        traffic_specs=["scenarios/sumo/loop/build/traffic/basic.rou.xml"],
    )
    return scenario


ego_alive_test = AgentsAliveDoneCriteria(
    minimum_ego_agents_alive=2,
)

custom_agent_list_test = AgentsAliveDoneCriteria(
    agent_lists_alive=[
        AgentsListAlive(
            agents_list=[AGENT1, AGENT2], minimum_agents_alive_in_list=1
        ),                                               
        AgentsListAlive(
            agents_list=[AGENT3], minimum_agents_alive_in_list=1
        ),                               
    ]
)

total_alive_test = AgentsAliveDoneCriteria(
    minimum_total_agents_alive=2,
)


@pytest.fixture(
    scope="module", params=[ego_alive_test, custom_agent_list_test, total_alive_test]
)
def sim(request):
    shared_interface = AgentInterface(
        done_criteria=DoneCriteria(agents_alive=request.param)
    )
    agents = {
        AGENT1: shared_interface,
        AGENT2: shared_interface,
        AGENT3: shared_interface,
    }
    smarts = SMARTS(
        agents,
        traffic_sims=[SumoTrafficSimulation(headless=True)],
        envision=None,
    )

    yield smarts
    smarts.destroy()


def test_agents_alive_done_check(sim, scenario):
    sim.setup(scenario)
    interface = sim.agent_manager.agent_interface_for_agent_id(AGENT1)
    done_criteria = interface.done_criteria

    sim_frame: SimulationFrame = sim.cached_frame
                                                     
    assert not Sensors._agents_alive_done_check(
        sim_frame.ego_ids, sim_frame.potential_agent_ids, done_criteria.agents_alive
    )

    sim.agent_manager.teardown_ego_agents({AGENT2})
    del sim.cached_frame
    sim_frame: SimulationFrame = sim.cached_frame
                                                     
    assert not Sensors._agents_alive_done_check(
        sim_frame.ego_ids, sim_frame.potential_agent_ids, done_criteria.agents_alive
    )

    sim.agent_manager.teardown_ego_agents({AGENT3})
    del sim.cached_frame
    sim_frame: SimulationFrame = sim.cached_frame
                                                     
    assert Sensors._agents_alive_done_check(
        sim_frame.ego_ids, sim_frame.potential_agent_ids, done_criteria.agents_alive
    )

    sim.agent_manager.teardown_ego_agents({AGENT1})
    del sim.cached_frame
    sim_frame: SimulationFrame = sim.cached_frame
                                                     
    assert Sensors._agents_alive_done_check(
        sim_frame.ego_ids, sim_frame.potential_agent_ids, done_criteria.agents_alive
    )


def test_interest_done():
    waiting_interest_criteria = InterestDoneCriteria(("leader",), strict=False)
    strict_interest_criteria = InterestDoneCriteria(("leader",), strict=True)

    sensor_state = mock.Mock()
    sensor_state.seen_interest_actors = True
                                                                    
    assert Sensors._interest_done_check({}, sensor_state, strict_interest_criteria)
    assert Sensors._interest_done_check({}, sensor_state, waiting_interest_criteria)

    sensor_state = mock.Mock()
    sensor_state.seen_interest_actors = False
                                                                    
    assert Sensors._interest_done_check({}, sensor_state, strict_interest_criteria)
    assert not Sensors._interest_done_check({}, sensor_state, waiting_interest_criteria)

    sensor_state = mock.Mock()
    sensor_state.seen_interest_actors = False
                                                   
    assert not Sensors._interest_done_check(
        {"leader": ActorState("leader")}, sensor_state, strict_interest_criteria
    )
    assert not Sensors._interest_done_check(
        {"leader": ActorState("leader")}, sensor_state, waiting_interest_criteria
    )
