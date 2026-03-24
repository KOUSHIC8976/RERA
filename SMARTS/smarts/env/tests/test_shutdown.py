             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from unittest import mock

import gymnasium as gym
import pytest

from smarts.core.agent import Agent
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.smarts import SMARTSNotSetupError
from smarts.env.utils.action_conversion import ActionOptions
from smarts.zoo.agent_spec import AgentSpec

AGENT_ID = "AGENT-007"


def build_env(agent_spec):
    return gym.make(
        "smarts.env:hiway-v1",
                                                                       
        scenarios=["scenarios/sumo/loop"],
        agent_interfaces={AGENT_ID: agent_spec.interface},
        headless=True,
        seed=2008,
        action_options=ActionOptions.unformatted,
    )


def test_graceful_shutdown():
    """SMARTS should not throw any exceptions when shutdown."""
    agent_spec = AgentSpec(
        interface=AgentInterface.from_type(AgentType.Laner),
        agent_builder=lambda: Agent.from_function(lambda _: "keep_lane"),
    )
    env = build_env(agent_spec)
    agent = agent_spec.build_agent()
    obs, _ = env.reset()
    for _ in range(10):
        obs, _, _, _, _ = env.step({AGENT_ID: agent.act(obs)})

    env.close()


def test_graceful_interrupt(monkeypatch):
    """SMARTS should only throw a KeyboardInterript exception."""

    agent_spec = AgentSpec(
        interface=AgentInterface.from_type(AgentType.Laner),
        agent_builder=lambda: Agent.from_function(lambda _: "keep_lane"),
    )
    agent = agent_spec.build_agent()
    env = build_env(agent_spec)

    with pytest.raises(KeyboardInterrupt):
        obs, _ = env.reset()

        episode = 0
                                                                                
                                                                                
        with mock.patch(
            "smarts.core.sensor_manager.SensorManager.observe",
            side_effect=KeyboardInterrupt,
        ):
            for episode in range(10):
                obs, _, _, _, _ = env.step({AGENT_ID: agent.act(obs)})

        assert episode == 0, "SMARTS should have been interrupted, ending early"

    with pytest.raises(SMARTSNotSetupError):
        env.step({AGENT_ID: agent.act(obs)})
