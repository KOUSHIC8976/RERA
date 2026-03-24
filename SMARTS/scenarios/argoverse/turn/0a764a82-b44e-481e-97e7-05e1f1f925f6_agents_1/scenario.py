from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

                                                            
                                
                                        
                                    

scenario_id = "0a764a82-b44e-481e-97e7-05e1f1f925f6"                                               
scenario_path = None                                                          
duration = 11
ego_mission = [
    t.Mission(
        t.Route(
            begin=("road-395015353-395015556", 0, 0.4),
            end=("road-394994351", 0, 8.1),
        )
    )
]

traffic_histories = [
    t.TrafficHistoryDataset(
        name=f"argoverse_{scenario_id}",
        source_type="Argoverse",
        input_path=scenario_path,
    )
]

gen_scenario(
    t.Scenario(
        ego_missions=ego_mission,
        map_spec=t.MapSpec(source=f"{scenario_path}", lanepoint_spacing=1.0),
        traffic_histories=traffic_histories,
        scenario_metadata=t.ScenarioMetadata(
            scenario_difficulty=0.6,
            scenario_duration=duration,
        ),
    ),
    output_dir=Path(__file__).parent,
)
