                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from __future__ import annotations

import weakref
from typing import TYPE_CHECKING, Iterable, List, Sequence, Set

from .actor import ActorRole
from .controllers import ActionSpaceType
from .provider import Provider, ProviderManager, ProviderRecoveryFlags, ProviderState
from .scenario import Scenario
from .utils.file import replace

if TYPE_CHECKING:
    from .vehicle_state import VehicleState


class ExternalProvider(Provider):
    """A provider that is intended to be used for external intervention in the simulation.
    Vehicles managed by this provider cannot be hijacked by social agents
    and may have privileged VehicleStates."""

    def __init__(self, sim):
                                                  
        self._recovery_flags = super().recovery_flags
        self.set_manager(sim)
        self.reset()

    def set_manager(self, manager: ProviderManager):
        self._sim = weakref.ref(manager)

    @property
    def _sim_time(self) -> float:
        sim = self._sim()
        assert sim
                                         
                                                           
        return sim.elapsed_sim_time
                                        

    @property
    def _vehicle_index(self):
        sim = self._sim()
        assert sim
                                         
                                                           
        return sim.vehicle_index
                                        

    @property
    def recovery_flags(self) -> ProviderRecoveryFlags:
        return self._recovery_flags

    @recovery_flags.setter
    def recovery_flags(self, flags: ProviderRecoveryFlags):
        self._recovery_flags = flags

    def reset(self):
        self._ext_vehicle_states = []
        self._sent_states = None
        self._last_step_delta = None
        self._last_fresh_step = self._sim_time

    def state_update(
        self,
        vehicle_states: Sequence[VehicleState],
        step_delta: float,
    ):
        """Update vehicle states. Use `all_vehicle_states()` to look at previous states."""
        self._ext_vehicle_states = [
            replace(vs, source=self.source_str, role=ActorRole.External)
            for vs in vehicle_states
        ]
        self._last_step_delta = step_delta

    @property
    def actions(self) -> Set[ActionSpaceType]:
        return set()

    @property
    def _provider_state(self):
        dt = self._sim_time - self._last_fresh_step
        if id(self._ext_vehicle_states) != id(self._sent_states):
            self._last_fresh_step = self._sim_time
            self._sent_states = self._ext_vehicle_states
        return ProviderState(actors=self._ext_vehicle_states, dt=dt)

    def setup(self, scenario: Scenario) -> ProviderState:
        return self._provider_state

    def step(self, actions, dt: float, elapsed_sim_time: float) -> ProviderState:
        return self._provider_state

    def sync(self, provider_state: ProviderState):
        pass

    def teardown(self):
        self.reset()

    @property
    def all_vehicle_states(self) -> List[VehicleState]:
        """Get all current vehicle states."""
        result = []
        for vehicle in self._vehicle_index.vehicles:
            if vehicle.subscribed_to_accelerometer_sensor:
                linear_acc, angular_acc, _, _ = vehicle.accelerometer_sensor(
                    vehicle.state.linear_velocity,
                    vehicle.state.angular_velocity,
                    self._last_step_delta,
                )
            result.append(vehicle.state)
        return result

    def manages_actor(self, actor_id: str) -> bool:
        for vs in self._ext_vehicle_states:
            if vs.actor_id == actor_id:
                return True
        return False

    @property
    def actor_ids(self) -> Iterable[str]:
        """A set of actors that this provider manages.

        Returns:
            Iterable[str]: The actors this provider manages.
        """
        return set(vs.actor_id for vs in self._ext_vehicle_states)
