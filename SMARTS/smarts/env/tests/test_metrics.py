             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

import dataclasses
from unittest import mock

import gymnasium as gym
import numpy as np
import pytest

from smarts.core.agent_interface import AgentInterface, DoneCriteria
from smarts.core.controllers import ActionSpaceType
from smarts.core.coordinates import Heading, Point
from smarts.core.plan import EndlessGoal, Goal, NavigationMission, PositionalGoal, Start
from smarts.env.gymnasium.wrappers.metric.metrics import Metrics, MetricsError
from smarts.zoo.agent_spec import AgentSpec


def _intrfc_improper():
    return [
        {"accelerometer": False},
        {"max_episode_steps": None},
        {"neighborhood_vehicle_states": False},
        {"waypoint_paths": False},
        {
            "done_criteria": DoneCriteria(
                collision=False,
                off_road=True,
            )
        },
        {
            "done_criteria": DoneCriteria(
                collision=True,
                off_road=False,
            )
        },
    ]


@pytest.fixture
def get_agent_spec(request):
    base_intrfc = AgentInterface(
        action=ActionSpaceType.TargetPose,
        accelerometer=True,
        done_criteria=DoneCriteria(
            collision=True,
            off_road=True,
            off_route=False,
            on_shoulder=False,
            wrong_way=False,
            not_moving=False,
            agents_alive=None,
        ),
        max_episode_steps=5,
        neighborhood_vehicle_states=True,
        waypoint_paths=True,
    )
    return AgentSpec(interface=dataclasses.replace(base_intrfc, **request.param))


@pytest.fixture(scope="module")
def get_scenario(request):
    from pathlib import Path

    from smarts.sstudio.scenario_construction import build_scenario

    if request.param == "single_agent_intersection":
        scenario = str(
            Path(__file__).resolve().parents[3]
            / "scenarios"
            / "sumo"
            / "intersections"
            / "1_to_1lane_left_turn_c_agents_1"
        )
        num_agents = 1
    elif request.param == "multi_agent_merge":
        scenario = str(
            Path(__file__).resolve().parents[3]
            / "scenarios"
            / "sumo"
            / "merge"
            / "3lane_agents_2"
        )
        num_agents = 2

    build_scenario(scenario=scenario)

    return (scenario, num_agents)


@pytest.fixture
def make_env(get_agent_spec, get_scenario):
    env = gym.make(
        "smarts.env:hiway-v1",
        scenarios=[get_scenario[0]],
        agent_interfaces={
            f"AGENT_{agent_id}": get_agent_spec.interface
            for agent_id in range(get_scenario[1])
        },
        headless=True,
    )
    yield env
    env.close()


@pytest.mark.parametrize("get_agent_spec", _intrfc_improper(), indirect=True)
@pytest.mark.parametrize("get_scenario", ["single_agent_intersection"], indirect=True)
def test_improper_interface(make_env):

                                            
    with pytest.raises(AttributeError):
        env = Metrics(env=make_env)


@pytest.mark.parametrize("get_agent_spec", [{}], indirect=True)
@pytest.mark.parametrize("get_scenario", ["single_agent_intersection"], indirect=True)
def test_init(make_env):

                                              
    env = Metrics(env=make_env)

                                                            
    for elem in ["_scen", "_road_map", "_records", "smarts"]:
        with pytest.raises(AttributeError):
            getattr(env, elem)


def _mock_mission(start: Start, goal: Goal):
    def func(scenario_root, agents_to_be_briefed):
        return [NavigationMission(start=start, goal=goal)]

    return func


@pytest.mark.parametrize("get_agent_spec", [{}], indirect=True)
@pytest.mark.parametrize("get_scenario", ["single_agent_intersection"], indirect=True)
def test_reset(make_env):

                                                                       
    with mock.patch(
        "smarts.core.scenario.Scenario.discover_agent_missions",
        side_effect=_mock_mission(
            start=Start(position=np.array([0, 0, 0]), heading=Heading(0)),
            goal=EndlessGoal(),
        ),
    ):
        with pytest.raises(MetricsError):
            env = Metrics(env=make_env)
            env.reset()
        return


@pytest.mark.parametrize("get_agent_spec", [{}], indirect=True)
@pytest.mark.parametrize("get_scenario", ["single_agent_intersection"], indirect=True)
def test_end_in_off_road(make_env):

                                                                         
    env = Metrics(env=make_env)
    obs, _ = env.reset()
    agent_name = next(iter(env.agent_interfaces.keys()))
    dones = {"__all__": False}
    while not dones["__all__"]:
        actions = {
            agent_name: np.append(
                obs[agent_name]["ego_vehicle_state"]["position"][:2]
                + np.array([0.5, -0.8]),
                [obs[agent_name]["ego_vehicle_state"]["heading"], 0.1],
            )
        }
        obs, _, dones, _, _ = env.step(actions)
    assert obs[agent_name]["events"]["off_road"], (
        "Expected vehicle to go off road, but it did not. "
        f"Events: {obs[agent_name]['events']}."
    )
    env.score()

                                                     
    records = env.records()
    scen_name = next(iter(records.keys()))
    counts = records[scen_name][agent_name].counts
    assert counts.goals == 0
    assert counts.episodes == 1
    assert counts.steps == 3


@pytest.mark.parametrize(
    "get_agent_spec",
    [{"max_episode_steps": 27, "done_criteria": DoneCriteria(off_route=True)}],
    indirect=True,
)
@pytest.mark.parametrize("get_scenario", ["single_agent_intersection"], indirect=True)
def test_end_in_off_route(make_env):

                                                                             
           
                                                                                      
                                                                                       
                                                                                      
    with mock.patch(
        "smarts.core.scenario.Scenario.discover_agent_missions",
        side_effect=_mock_mission(
            start=Start(position=np.array([-12, -1.6, 0]), heading=Heading(-1.57)),
            goal=PositionalGoal(position=Point(x=1.5, y=30.5, z=0), radius=3),
        ),
    ):
        env = Metrics(env=make_env)
        obs, _ = env.reset()
        agent_name = next(iter(env.agent_interfaces.keys()))
        dones = {"__all__": False}
        while not dones["__all__"]:
            actions = {
                agent_name: np.append(
                    obs[agent_name]["ego_vehicle_state"]["position"][:2]
                    + np.array([1, 0]),
                    [obs[agent_name]["ego_vehicle_state"]["heading"], 0.1],
                )
            }
            obs, _, dones, _, _ = env.step(actions)
        assert (
            obs[agent_name]["ego_vehicle_state"]["lane_id"].rstrip() == "edge-east-WE_0"
        ), (
            "Expected vehicle to drive off route, but it is at lane: "
            f"{obs[agent_name]['ego_vehicle_state']['lane_id']}."
        )
        assert obs[agent_name]["events"]["off_route"], (
            "Expected vehicle to go off route, but it did not. "
            f"Events: {obs[agent_name]['events']}."
        )
        env.score()


@pytest.mark.parametrize("get_agent_spec", [{"max_episode_steps": 1}], indirect=True)
@pytest.mark.parametrize("get_scenario", ["single_agent_intersection"], indirect=True)
def test_end_in_junction(make_env):

                                                                              
           
                                                                                            
    with mock.patch(
        "smarts.core.scenario.Scenario.discover_agent_missions",
        side_effect=_mock_mission(
            start=Start(position=np.array([-1.86, 1.95, 0]), heading=Heading(-1.00)),
            goal=PositionalGoal(position=Point(x=1.5, y=30.5, z=0), radius=3),
        ),
    ):
        env = Metrics(env=make_env)
        obs, _ = env.reset()
        agent_name = next(iter(obs.keys()))
        actions = {
            agent_id: np.array([-1.76, 2.05, -0.91, 0.1]) for agent_id in obs.keys()
        }
        obs, _, dones, _, _ = env.step(actions)
        assert (
            obs[agent_name]["ego_vehicle_state"]["lane_id"].rstrip()
            == ":junction-intersection_1_0"
        ), (
            "Expected vehicle to be inside junction, but it is at lane: "
            f"{obs[agent_name]['ego_vehicle_state']['lane_id']}."
        )
        assert (
            obs[agent_name]["events"]["reached_max_episode_steps"] and dones["__all__"]
        ), (
            "Expected vehicle to reach max episode steps and become done, but "
            f"it did not. Dones: {dones}. Events: {obs[agent_name]['events']}."
        )
        env.score()


@pytest.mark.parametrize("get_agent_spec", [{}], indirect=True)
@pytest.mark.parametrize("get_scenario", ["multi_agent_merge"], indirect=True)
def test_records_and_scores(make_env):

                                                                               
           
                                                                                     
    env = Metrics(env=make_env)
    obs, _ = env.reset()
    terminated = {"__all__": False}
    while not terminated["__all__"]:
        actions = {
            agent_name: np.append(
                agent_obs["ego_vehicle_state"]["position"][:2], [0, 0.1]
            )
            for agent_name, agent_obs in obs.items()
        }
        obs, _, terminated, _, _ = env.step(actions)
    env.records()
    env.score()
