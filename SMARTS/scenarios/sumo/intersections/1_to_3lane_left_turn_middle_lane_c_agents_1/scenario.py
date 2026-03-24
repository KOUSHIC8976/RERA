                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import random
from itertools import combinations
from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio.sstypes import (
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
)

vertical_routes = [
    ("E2", 0, "E7", 0),
    ("E8", 0, "E1", 1),
]

horizontal_routes = [
    ("E3", 0, "E5", 0),
    ("E3", 1, "E5", 1),
    ("E3", 2, "E5", 2),
    ("E6", 1, "E4", 1),
    ("E6", 0, "E4", 0),
]

turn_left_routes = [
    ("E8", 0, "E5", 2),
    ("E6", 1, "E1", 1),
    ("E2", 1, "E4", 1),
    ("E3", 2, "E7", 0),
]

turn_right_routes = [
    ("E6", 0, "E7", 0),
    ("E3", 0, "E1", 0),
    ("E2", 0, "E5", 0),
    ("E8", 0, "E4", 0),
]

                          
all_routes = vertical_routes + horizontal_routes + turn_left_routes + turn_right_routes
route_comb = [com for elems in range(4, 5) for com in combinations(all_routes, elems)]
traffic = {}
for name, routes in enumerate(route_comb):
    traffic[str(name)] = Traffic(
        flows=[
            Flow(
                route=Route(
                    begin=(f"{r[0]}", r[1], 0),
                    end=(f"{r[2]}", r[3], "max"),
                ),
                                                                        
                rate=60 * random.uniform(5, 10),
                                                                  
                begin=random.uniform(0, 3),
                                                                         
                                                                             
                                                                            
                       
                end=60 * 15,
                actors={normal: 1},
            )
            for r in routes
        ]
    )

route = Route(begin=("E8", 0, 5), end=("E5", 1, "max"))
default_speed = 13
route_length = 100
duration = (route_length / default_speed) * 2
ego_missions = [
    Mission(
        route=route,
        start_time=15,                                                    
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
