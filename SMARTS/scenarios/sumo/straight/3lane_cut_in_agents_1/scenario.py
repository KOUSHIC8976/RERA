                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import random
from itertools import combinations
from pathlib import Path

from numpy import random

from smarts.sstudio import gen_scenario
from smarts.sstudio.sstypes import (
    Distribution,
    Flow,
    Mission,
    Route,
    Scenario,
    SmartsLaneChangingModel,
    Traffic,
    TrafficActor,
    TrapEntryTactic,
)

normal = TrafficActor(
    name="car",
    sigma=1,
    speed=Distribution(sigma=0.1, mean=1.5),
    min_gap=Distribution(sigma=0, mean=1),
    lane_changing_model=SmartsLaneChangingModel(
        cutin_prob=1, assertive=10, dogmatic=True, slow_down_after=0.5
    ),
)

                                    
route_opt = [
    (0, 0),
    (1, 1),
    (2, 2),
]

                                              
                                               
min_flows = 3
max_flows = 3
route_comb = [
    com
    for elems in range(min_flows, max_flows + 1)
    for com in combinations(route_opt, elems)
] * 100

traffic = {}
for name, routes in enumerate(route_comb):
    traffic[str(name)] = Traffic(
        engine="SMARTS",
        flows=[
            Flow(
                route=Route(
                    begin=("gneE3", start_lane, 0),
                    end=("gneE3", end_lane, "max"),
                ),
                                                                        
                rate=60 * random.uniform(6, 14),
                                                                  
                begin=random.uniform(0, 5),
                                                                         
                                                                             
                                                                           
                               
                end=60 * 15,
                actors={normal: 1},
                randomly_spaced=True,
            )
            for start_lane, end_lane in routes
        ],
    )


route = Route(begin=("gneE3", 1, 10), end=("gneE3", 1, "max"))
ego_missions = [
    Mission(
        route=route,
        entry_tactic=TrapEntryTactic(
            start_time=20
        ),                                                    
    )
]

gen_scenario(
    scenario=Scenario(
        traffic=traffic,
        ego_missions=ego_missions,
    ),
    output_dir=Path(__file__).parent,
)
