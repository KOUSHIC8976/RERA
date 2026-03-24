                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio.sstypes import Mission, RandomRoute, Scenario, SocialAgentActor


def gen_actors(id_):
    return [
        SocialAgentActor(
            name=f"non-interactive-agent-50-v0_{id_}",
            agent_locator="zoo.policies:non-interactive-agent-v0",
            policy_kwargs={"speed": 50},
        )
    ]


def to_missions(agent_num):
    missions = {}
    for i in range(0, agent_num):
        missions[f"group-{i}"] = tuple(
            (gen_actors(i), [Mission(route=RandomRoute())]),
        )
    return missions


gen_scenario(
    Scenario(
        social_agent_missions=to_missions(10),
    ),
    output_dir=Path(__file__).parent,
)
