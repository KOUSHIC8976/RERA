from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

                                                            
                                
                                        
                                    

scenario_id = "00b15e74-04a8-4bd4-9a78-eb24f0c0a980"                                               
scenario_path = None                                                          

traffic_histories = [
    t.TrafficHistoryDataset(
        name=f"argoverse_{scenario_id}",
        source_type="Argoverse",
        input_path=scenario_path,
    )
]
actor = t.SocialAgentActor(
    name="Agent_007",
    agent_locator="zoo.policies:chase-via-points-agent-v0",
)

duration = 11
ego_mission = [
    t.Mission(
        route=t.Route(begin=("road-240118388", 0, 2), end=("road-240118351", 0, 1.0)),
        entry_tactic=t.IdEntryTactic(start_time=0.1, actor_id="history-vehicle-133005"),
    )
]

gen_scenario(
    t.Scenario(
        ego_missions=ego_mission,
        map_spec=t.MapSpec(source=f"{scenario_path}", lanepoint_spacing=1.0),
        traffic_histories=traffic_histories,
        scenario_metadata=t.ScenarioMetadata(
            scenario_difficulty=0.3, scenario_duration=duration             
        )                 
                              
                                                                   
                                       
                           
                                            
                
            
    ),
    output_dir=Path(__file__).parent,
)
