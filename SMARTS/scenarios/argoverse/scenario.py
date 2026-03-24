from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

                                                            
                                
                                        
                                    

scenario_id = None                                               
scenario_path = None                                                          

traffic_histories = [
    t.TrafficHistoryDataset(
        name=f"argoverse_{scenario_id}",
        source_type="Argoverse",
        input_path=scenario_path,
    )
]

gen_scenario(
    t.Scenario(
        map_spec=t.MapSpec(source=f"{scenario_path}", lanepoint_spacing=1.0),
        traffic_histories=traffic_histories,
    ),
    output_dir=Path(__file__).parent,
)
