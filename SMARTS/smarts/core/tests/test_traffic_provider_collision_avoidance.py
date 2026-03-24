             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import pytest

                                 
from helpers.scenario import temp_scenario

import smarts.sstudio.sstypes as t
from smarts.core.local_traffic_provider import LocalTrafficProvider
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.sstudio import gen_scenario


@pytest.fixture(params=["SUMO", "SMARTS"])
def traffic_sim(request):
    return getattr(request, "param", "SUMO")


@pytest.fixture
def scenarios(traffic_sim):
    with temp_scenario(name="6lane", map="maps/t.net.xml") as scenario_root:
        traffic = t.Traffic(
            engine=traffic_sim,
            flows=[
                t.Flow(
                    route=t.Route(
                        begin=("edge-west-WE", 0, 10),
                        end=("edge-east-WE", 1, "max"),
                    ),
                    repeat_route=True,
                    rate=400,
                    actors={t.TrafficActor("car"): 1},
                ),
                t.Flow(
                    route=t.Route(
                        begin=("edge-south-SN", 1, 10),
                        end=("edge-west-EW", 1, "max"),
                    ),
                    repeat_route=True,
                    rate=400,
                    actors={t.TrafficActor("car"): 1},
                ),
            ],
        )

        gen_scenario(
            t.Scenario(traffic={"all": traffic}),
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


                                                                 
@pytest.mark.parametrize("traffic_sim", ["SUMO", "SMARTS"], indirect=True)
def test_collision_avoidance_in_intersection(smarts, scenarios, traffic_sim):
    """Ensure that traffic providers can manage basic collision avoidance around an intersection."""
    scenario = next(scenarios)
    smarts.reset(scenario)

    for _ in range(1000):
        smarts.step({})
        assert not smarts._vehicle_collisions
