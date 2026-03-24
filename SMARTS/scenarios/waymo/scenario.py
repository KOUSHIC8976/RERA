from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

dataset_path = None                                                                                                   
scenario_id = None                           

traffic_histories = [
    t.TrafficHistoryDataset(
        name=f"waymo",
        source_type="Waymo",
        input_path=dataset_path,
        scenario_id=scenario_id,
    )
]

gen_scenario(
    t.Scenario(
        map_spec=t.MapSpec(
            source=f"{dataset_path}#{scenario_id}", lanepoint_spacing=1.0
        ),
        traffic_histories=traffic_histories,
    ),
    output_dir=Path(__file__).parent,
)
