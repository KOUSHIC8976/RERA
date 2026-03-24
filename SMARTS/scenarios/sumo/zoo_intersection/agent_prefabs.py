from smarts.core.agent import Agent
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.zoo.agent_spec import AgentSpec
from smarts.zoo.registry import register


class SimpleAgent(Agent):
    def act(self, obs):
        return "keep_lane"


                                                            
def demo_agent_callable(target_prefix=None, interface=None):
    if interface is None:
        interface = AgentInterface.from_type(AgentType.Laner)
    return AgentSpec(interface=interface, agent_builder=SimpleAgent)


register(
    locator="zoo-agent1-v0",
    entry_point="smarts.zoo.agent_spec:AgentSpec",
                 
                                                 
    interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=20000),
)

register(
    locator="zoo-agent2-v0",
    entry_point=demo_agent_callable,
                 
                                                                        
)
