             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


from dataclasses import dataclass
from typing import Optional, Tuple

from smarts.core.condition_state import ConditionState
from smarts.sstudio.sstypes.condition import (
    Condition,
    ConditionRequires,
    LiteralCondition,
)
from smarts.sstudio.sstypes.zone import MapZone


@dataclass(frozen=True)
class EntryTactic:
    """The tactic that the simulation should use to acquire a vehicle for an agent."""

    start_time: float

    def __post_init__(self):
        assert (
            getattr(self, "condition", None) is not None
        ), "Abstract class, inheriting types must implement the `condition` field."


@dataclass(frozen=True)
class TrapEntryTactic(EntryTactic):
    """An entry tactic that repurposes a pre-existing vehicle for an agent."""

    wait_to_hijack_limit_s: float = 0
    """The amount of seconds a hijack will wait to get a vehicle before defaulting to a new vehicle"""
    zone: Optional[MapZone] = None
    """The zone of the hijack area"""
    exclusion_prefixes: Tuple[str, ...] = tuple()
    """The prefixes of vehicles to avoid hijacking"""
    default_entry_speed: Optional[float] = None
    """The speed that the vehicle starts at when the hijack limit expiry emits a new vehicle"""
    condition: Condition = LiteralCondition(ConditionState.TRUE)
    """A condition that is used to add additional exclusions."""

    def __post_init__(self):
        assert isinstance(self.condition, (Condition))
        assert not (
            self.condition.requires & ConditionRequires.any_current_actor_state
        ), f"Trap entry tactic cannot use conditions that require any_vehicle_state."


@dataclass(frozen=True)
class IdEntryTactic(EntryTactic):
    """An entry tactic which repurposes a pre-existing actor for an agent. Selects that actor by id."""

    actor_id: str
    """The id of the actor to take over."""

    condition: Condition = LiteralCondition(ConditionState.TRUE)
    """A condition that is used to add additional exclusions."""

    def __post_init__(self):
        assert isinstance(self.actor_id, str)
        assert isinstance(self.condition, (Condition))
