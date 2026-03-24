                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import random
from itertools import combinations
from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio.sstypes import (
    Distribution,
    Flow,
    Mission,
    Route,
    Scenario,
    Traffic,
    TrafficActor,
    TrapEntryTactic,
)

normal = TrafficActor(
    name="car",
    max_speed=10,
    min_gap=Distribution(mean=4, sigma=1.2),
)

                                    
route_opt = [
    (0, 0),
]

                                
                                               
min_flows = 1
max_flows = 1
route_comb = [
    com
    for elems in range(min_flows, max_flows + 1)
    for com in combinations(route_opt, elems)
] * 400

traffic = {}
for name, routes in enumerate(route_comb):
    traffic[str(name)] = Traffic(
        flows=[
            Flow(
                route=Route(
                    begin=("gneE3", start_lane, 0),
                    end=("gneE3", end_lane, "max"),
                ),
                                                                        
                rate=60 * random.uniform(10, 20),
                                                                  
                begin=random.uniform(0, 5),
                                                                         
                                                                             
                                                                           
                               
                end=60 * 15,
                actors={normal: 1},
                randomly_spaced=True,
            )
            for start_lane, end_lane in routes
        ]
    )

route = Route(begin=("gneE3", 0, 10), end=("gneE3", 0, "max"))
ego_missions = [
    Mission(
        route=route,
        entry_tactic=TrapEntryTactic(
            start_time=17
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
