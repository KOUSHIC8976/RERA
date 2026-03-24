             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import logging
import os
import tempfile

import gymnasium as gym
import importlib_resources
import pytest
import pytest_notebook.nb_regression as nb

from smarts.core.agent import Agent
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.observations import Observation
from smarts.core.utils.episodes import episodes
from smarts.zoo.agent_spec import AgentSpec

logging.basicConfig(level=logging.INFO)

AGENT_ID = "Agent-007"
NOTEBOOK_NAME = "test_notebook.ipynb"


class KeepLaneAgent(Agent):
    def act(self, obs: Observation):
        return "keep_lane"


def run_scenario(
    scenarios,
    sim_name,
    headless,
    num_episodes,
    seed,
    max_episode_steps=None,
):
    agent_spec = AgentSpec(
        interface=AgentInterface.from_type(
            AgentType.Laner, max_episode_steps=max_episode_steps
        ),
        agent_builder=KeepLaneAgent,
    )

    env = gym.make(
        "smarts.env:hiway-v1",
        scenarios=scenarios,
        agent_specs={AGENT_ID: agent_spec.interface},
        sim_name=sim_name,
        headless=headless,
        fixed_timestep_sec=0.1,
        seed=seed,
    )

    for episode in episodes(n=num_episodes):
        agent = agent_spec.build_agent()
        observations, _ = env.reset()
        episode.record_scenario(env.scenario_log)

        terminateds = {"__all__": False}
        while not terminateds["__all__"]:
            agent_obs = observations[AGENT_ID]
            agent_action = agent.act(agent_obs)
            observations, rewards, terminateds, truncateds, infos = env.step(
                {AGENT_ID: agent_action}
            )
            episode.record_step(observations, rewards, terminateds, truncateds, infos)

    env.close()


@pytest.fixture(scope="module")
def notebook():
    _, tmppath = tempfile.mkstemp(suffix=".ipynb")
    with open(tmppath, "w") as f:
        import smarts.core.tests

                                     
        traversable = importlib_resources.files(smarts.core.tests)
        f.write(traversable.joinpath(NOTEBOOK_NAME).read_text())
                                    
    yield tmppath
    os.remove(tmppath)


def test_notebook1(nb_regression: nb.NBRegressionFixture, notebook):

                                        
    nb_regression.force_regen = True
    try:
        nb_regression.check(notebook, False)
    except TimeoutError as te:
        assert (
            False
        ), f"pynotebook `{NOTEBOOK_NAME}` timed out after {nb_regression.exec_timeout}s during test: {te}.\nFor more details see: https://jupyterbook.org/content/execute.html#setting-execution-timeout"
                                     
                            
    nb_regression.diff_ignore = (
        "/cells/*/outputs/*/text",
        "/metadata/language_info/version",
    )
    nb_regression.force_regen = False
    nb_regression.check(notebook)
