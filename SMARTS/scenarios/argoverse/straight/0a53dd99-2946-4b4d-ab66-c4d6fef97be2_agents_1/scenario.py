from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

                                                            
                                
                                        
                                    


scenario_id = "0a53dd99-2946-4b4d-ab66-c4d6fef97be2"                                               
scenario_path = None                                                          

ego_mission = [
    t.Mission(
        t.Route(
            begin=("road-353638670-353638219-353638558", 1, 6.7),
            end=("road-353637909-353637861-353637941-353637727", 1, 4.2),
        ),
        entry_tactic=t.IdEntryTactic(start_time=0.1, actor_id="history-vehicle-5717"),
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
