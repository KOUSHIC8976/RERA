             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import os
import tempfile
from typing import Sequence
from xml.etree.ElementTree import ElementTree

import pytest

from smarts.core.scenario import Scenario
from smarts.sstudio.genscenario import gen_map_spec_artifact, gen_traffic
from smarts.sstudio.sstypes import (
    Distribution,
    Flow,
    JunctionModel,
    LaneChangingModel,
    MapSpec,
    Mission,
    Route,
    Traffic,
    TrafficActor,
)


@pytest.fixture
def traffic() -> Traffic:
    car1 = TrafficActor(
        name="car",
        speed=Distribution(sigma=0.2, mean=1.0),
    )
    car2 = TrafficActor(
        name="car",
        speed=Distribution(sigma=0.2, mean=0.8),
        lane_changing_model=LaneChangingModel(impatience=1, cooperative=0.25),
        junction_model=JunctionModel(drive_after_yellow_time=1.0, impatience=0.5),
    )

    return Traffic(
        flows=[
            Flow(
                route=Route(
                    begin=(f"edge-{r[0]}", 0, 30), end=(f"edge-{r[1]}", 0, -30)
                ),
                rate=1.0,
                actors={
                    car1: 0.5,
                    car2: 0.5,
                },
            )
            for r in [("west-WE", "east-WE"), ("east-EW", "west-EW")]
        ]
    )


@pytest.fixture
def missions() -> Sequence[Mission]:
    return [
        Mission(Route(begin=("edge-west-WE", 0, 0), end=("edge-south-NS", 0, 0))),
        Mission(Route(begin=("edge-south-SN", 0, 30), end=("edge-west-EW", 0, 0))),
    ]


def test_generate_traffic(traffic: Traffic):
    with tempfile.TemporaryDirectory() as temp_dir:
        gen_traffic(
            "scenarios/sumo/intersections/4lane_t",
            traffic,
            output_dir=temp_dir,
            name="generated",
        )

        _compare_files(
            "smarts/sstudio/tests/baseline.rou.xml",
            os.path.join(temp_dir, "traffic", "generated.rou.xml"),
        )


def _compare_files(file1, file2):
    with open(file1, encoding="UTF-8") as f:
        items = [x.items() for x in ElementTree(file=f).iter()]

    with open(file2, encoding="UTF-8") as f:
        generated_items = [x.items() for x in ElementTree(file=f).iter()]

    sorted_items = sorted(items)
    sorted_generated_items = sorted(generated_items)
    if not sorted_items == sorted_generated_items:
        for a, b in zip(sorted_items, sorted_generated_items):
            assert a == b, f"{file1} is different than {file2}"


def _gen_map_from_spec(scenario_root: str, map_spec: MapSpec):
    with tempfile.TemporaryDirectory() as temp_dir:
        gen_map_spec_artifact(scenario_root, map_spec, output_dir=temp_dir)
        found_map_spec = Scenario.discover_map(temp_dir)
        assert found_map_spec
        road_map = found_map_spec.builder_fn(found_map_spec)
        assert road_map


def test_generate_sumo_map():
    scenario_root = "scenarios/sumo/intersections/4lane_t"
    map_file = "map.net.xml"

    map_path = os.path.join(scenario_root, map_file)
    map_spec = MapSpec(map_path)
    _gen_map_from_spec(scenario_root, map_spec)

    lw = 5.2
    lps = 3.14

    def fake_map_builder(map_spec: MapSpec) -> bool:
        assert map_spec.source == map_path
        assert map_spec.default_lane_width == lw
        assert map_spec.lanepoint_spacing == lps
        return True

    map_spec = MapSpec(map_path, lps, lw, fake_map_builder)
    _gen_map_from_spec(scenario_root, map_spec)


def test_generate_od_map():
    scenario_root = "scenarios/open_drive/od_4lane"
    map_file = "map.xodr"

    map_path = os.path.join(scenario_root, map_file)
    map_spec = MapSpec(map_path)
    _gen_map_from_spec(scenario_root, map_spec)

    lw = 3.7
    lps = 1.0

    def fake_map_builder(map_spec: MapSpec) -> bool:
        assert map_spec.source == map_path
        assert map_spec.default_lane_width == lw
        assert map_spec.lanepoint_spacing == lps
        return True

    map_spec = MapSpec(map_path, lps, lw, fake_map_builder)
    _gen_map_from_spec(scenario_root, map_spec)
