             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from typing import Any

import pytest

from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.controllers import ActionSpaceType
from smarts.core.plan import NavigationMission
from smarts.core.scenario import Scenario
from smarts.core.sensors import Observation
from smarts.core.sensors.parallel_sensor_resolver import (
    SensorsWorker,
    SensorsWorkerRequestId,
    WorkerKwargs,
)
from smarts.core.simulation_frame import SimulationFrame
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.core.utils.core_logging import diff_unpackable

SimulationState = SimulationFrame
SensorState = Any

AGENT_IDS = [f"agent-00{i}" for i in range(100)]


@pytest.fixture
def scenario() -> Scenario:
    s = Scenario(
        scenario_root="scenarios/sumo/loop",
        traffic_specs=["scenarios/sumo/loop/build/traffic/basic.rou.xml"],
        missions=dict(
            zip(
                AGENT_IDS,
                Scenario.discover_agent_missions(
                    scenario_root="scenarios/sumo/loop",
                    agents_to_be_briefed=AGENT_IDS,
                ),
            )
        ),
    )
    missions = [
        NavigationMission.random_endless_mission(
            s.road_map,
        )
        for _ in AGENT_IDS
    ]
    s.set_ego_missions(dict(zip(AGENT_IDS, missions)))
    return s


@pytest.fixture(
    params=[
        AgentInterface.from_type(
            AgentType.Laner,
            action=ActionSpaceType.Continuous,
        ),
        AgentInterface.from_type(
            AgentType.Full,
            action=ActionSpaceType.Continuous,
        ),
    ]
)
def sim(scenario, request):
    a_interface = getattr(request, "param")
    agents = {aid: a_interface for aid in AGENT_IDS}
    smarts = SMARTS(
        agents,
        traffic_sims=[SumoTrafficSimulation(headless=True)],
        envision=None,
    )
    smarts.reset(scenario)
    smarts.step({aid: [0, 0, 0] for aid in AGENT_IDS})
    yield smarts
    smarts.destroy()


def test_sensor_worker(
    sim: SMARTS,
):
    del sim.cached_frame
    sim_frame: SimulationFrame = sim.cached_frame
    agent_ids = set(AGENT_IDS)
    worker = SensorsWorker()
    worker.run()
    worker.send(
        request=SensorsWorker.Request(
            SensorsWorkerRequestId.SIMULATION_LOCAL_CONSTANTS,
            WorkerKwargs(sim_local_constants=sim.local_constants),
        )
    )
    assert worker.running
    worker_args = WorkerKwargs(sim_frame=sim_frame, agent_ids=agent_ids)
    worker.send(
        SensorsWorker.Request(SensorsWorkerRequestId.SIMULATION_FRAME, worker_args)
    )
    state = dict(
        sim_frame=sim_frame,
        sim_local_constants=sim.local_constants,
        agent_ids=agent_ids,
    )
    observations, dones, updated_sensors = SensorsWorker.local(state=state)
    other_observations, other_dones, updated_sensors = worker.result(timeout=5)

    assert isinstance(observations, dict)
    assert all(
        [isinstance(obs, Observation) for obs in observations.values()]
    ), f"{observations}"
    assert isinstance(dones, dict)
    assert all([isinstance(obs, bool) for obs in dones.values()])
    assert isinstance(other_observations, dict)
    assert all([isinstance(obs, Observation) for obs in other_observations.values()])
    assert isinstance(other_dones, dict)
    assert all([isinstance(obs, bool) for obs in other_dones.values()])
    assert observations.keys() == other_dones.keys()
    assert diff_unpackable(other_observations, observations) == ""
