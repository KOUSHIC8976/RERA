                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from smarts.core.utils.class_factory import ClassRegister

agent_registry = ClassRegister()


def register(locator: str, entry_point, **kwargs):
    """Register an AgentSpec with the zoo.

    In order to load a registered AgentSpec it needs to be reachable from a
    directory contained in the PYTHONPATH.

    Args:
        locator:
            A string in the format of 'locator-name'
        entry_point:
            A callable that returns an AgentSpec or an AgentSpec object

    For example:

    .. code-block:: python

        register(
            locator="motion-planner-agent-v0",
            entry_point=lambda **kwargs: AgentSpec(
                interface=AgentInterface(waypoint_paths=True, action=ActionSpaceType.TargetPose),
                agent_builder=MotionPlannerAgent,
            ),
        )
    """

    agent_registry.register(name=locator, entry_point=entry_point, **kwargs)


def make(locator: str, **kwargs):
    """Create an AgentSpec from the given locator.

    In order to load a registered AgentSpec it needs to be reachable from a
    directory contained in the PYTHONPATH.

    Args:
        locator:
            A string in the format of 'path.to.file:locator-name' where the path
            is in the form `{PYTHONPATH}[n]/path/to/file.py`
        kwargs:
            Additional arguments to be passed to the constructed class.
    Returns:
        AgentSpec: The agent specifications needed to instantiate and configure an agent.
    """

    from smarts.zoo.agent_spec import AgentSpec

    agent_spec = agent_registry.make(locator, **kwargs)
    assert isinstance(
        agent_spec, AgentSpec
    ), f"Expected make to produce an instance of AgentSpec, got: {agent_spec}"

    return agent_spec


def make_agent(locator: str, **kwargs):
    """Create an Agent from the given agent spec locator.

    In order to load a registered AgentSpec it needs to be reachable from a
    directory contained in the PYTHONPATH.

    Args:
        locator:
            A string in the format of 'path.to.file:locator-name' where the path
            is in the form `{PYTHONPATH}[n]/path/to/file.py`
        kwargs:
            Additional arguments to be passed to the constructed class.
    Returns:
        Tuple[Agent, AgentInterface]: The agent and its interface.
    """

    agent_spec = make(locator, **kwargs)

    return agent_spec.build_agent(), agent_spec.interface
