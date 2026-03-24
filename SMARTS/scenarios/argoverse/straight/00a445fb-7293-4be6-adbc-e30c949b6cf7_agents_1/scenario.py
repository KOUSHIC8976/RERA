from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

                                                            
                                
                                        
                                    


scenario_id = "00a445fb-7293-4be6-adbc-e30c949b6cf7"                                               
scenario_path = None                                                          

ego_mission = [
    t.Mission(
        t.Route(
            begin=("road-206498749-206498861", 0, 28.3),
            end=("road-206498749-206498861", 0, 52.3),
        ),
        entry_tactic=t.TrapEntryTactic(
            start_time=0.1, wait_to_hijack_limit_s=0, default_entry_speed=0
        ),
    )
]

traffic_histories = [
    t.TrafficHistoryDataset(
        name=f"argoverse_{scenario_id}",
        source_type="Argoverse",
        input_path=scenario_path,
    )
]
duration = 11
gen_scenario(
    t.Scenario(
        ego_missions=ego_mission,
        map_spec=t.MapSpec(source=f"{scenario_path}", lanepoint_spacing=1.0),
        traffic_histories=traffic_histories,
        scenario_metadata=t.ScenarioMetadata(
            scenario_difficulty=0.3,
            scenario_duration=duration,
        ),
    ),
    output_dir=Path(__file__).parent,
)
