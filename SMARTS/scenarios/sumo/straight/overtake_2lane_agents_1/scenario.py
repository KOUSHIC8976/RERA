                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

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
    ScenarioMetadata,
    Traffic,
    TrafficActor,
)

normal = TrafficActor(
    name="car",
    speed=Distribution(sigma=0.2, mean=0.5),
)

                                     
route_opt = [
    (0, 0),
    (1, 1),
]

                      
min_flows = 2
max_flows = 2
route_comb = [
    com
    for elems in range(min_flows, max_flows + 1)
    for com in combinations(route_opt, elems)
] * 100

traffic = {}
for name, routes in enumerate(route_comb):
    traffic[str(name)] = Traffic(
        flows=[
            Flow(
                route=Route(
                    begin=("gneE3", r[0], 0),
                    end=("gneE3", r[1], "max"),
                ),
                                                                        
                rate=60 * random.uniform(5, 10),
                                                                  
                begin=random.uniform(0, 5),
                                                                         
                                                                             
                                                                            
                       
                end=60 * 15,
                actors={normal: 1},
                randomly_spaced=True,
            )
            for r in routes
        ]
    )

default_speed = 13
route_length = 200
duration = (route_length / default_speed) * 2
route = Route(begin=("gneE3", 0, 5), end=("gneE3", 1, "max"))
ego_missions = [
    Mission(
        route=route,
        start_time=17,                                                    
    )
]
              
gen_scenario(
    scenario=Scenario(
        traffic=traffic,
        ego_missions=ego_missions,
        scenario_metadata=ScenarioMetadata(
            scenario_difficulty=0.6,
            scenario_duration=duration,
        ),
    ),
    output_dir=Path(__file__).parent,
)
