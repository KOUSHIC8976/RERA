                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from typing import Dict, Iterable, Optional, Set, Tuple

from .actor import ActorRole, ActorState
from .controllers import ActionSpaceType
from .provider import Provider, ProviderManager, ProviderRecoveryFlags, ProviderState
from .road_map import RoadMap
from .scenario import Scenario
from .signals import SignalLightState, SignalState


class SignalProvider(Provider):
    """A SignalProvider manages traffic light signals."""

    def __init__(self):
        self._my_signals: Dict[str, SignalState] = dict()
                                                  
        self._recovery_flags = super().recovery_flags
        self._road_map = None

    @property
    def recovery_flags(self) -> ProviderRecoveryFlags:
        return self._recovery_flags

    @recovery_flags.setter
    def recovery_flags(self, flags: ProviderRecoveryFlags):
        self._recovery_flags = flags

    @property
    def actions(self) -> Set[ActionSpaceType]:
                                                                            
                                                                             
        return set()

    def set_manager(self, manager: ProviderManager):
        pass

    @property
    def _provider_state(self) -> ProviderState:
        return ProviderState(actors=list(self._my_signals.values()))

    def setup(self, scenario: Scenario) -> ProviderState:
        self._road_map = scenario.road_map
                                                                                           
                                                                                                
                                                                                                                                     
        if scenario.traffic_history is None and not scenario.supports_sumo_traffic:
            for feature in self._road_map.dynamic_features:
                if feature.type == RoadMap.FeatureType.FIXED_LOC_SIGNAL:
                    feature_lane = feature.type_specific_info
                    controlled_lanes = [feature_lane.lane_id]
                    self._my_signals[feature.feature_id] = SignalState(
                        actor_id=feature.feature_id,
                        actor_type="signal",
                        source=self.source_str,
                        role=ActorRole.Signal,
                        state=SignalLightState.UNKNOWN,
                        stopping_pos=feature.geometry[0],
                        controlled_lanes=controlled_lanes,
                        last_changed=None,
                    )
        return self._provider_state

    def step(self, actions, dt: float, elapsed_sim_time: float) -> ProviderState:
                                                                                                        
        return self._provider_state

    def sync(self, provider_state: ProviderState):
        for actor_state in provider_state.actors:
            if actor_state.actor_id in self._my_signals:
                assert isinstance(actor_state, SignalState)
                self._my_signals[actor_state.actor_id] = actor_state

    def can_accept_actor(self, state: ActorState) -> bool:
        return isinstance(state, SignalState)

    def add_actor(
        self, provider_actor: ActorState, from_provider: Optional[Provider] = None
    ):
        assert isinstance(provider_actor, SignalState)
        self._my_signals[provider_actor.actor_id] = provider_actor

    def reset(self):
        pass

    def teardown(self):
        self._my_signals = dict()

    def manages_actor(self, actor_id: str) -> bool:
        return actor_id in self._my_signals

    def stop_managing(self, actor_id: str):
        if actor_id in self._my_signals:
            del self._my_signals[actor_id]

    @property
    def actor_ids(self) -> Iterable[str]:
        """A set of actors that this provider manages.

        Returns:
            Iterable[str]: The actors this provider manages.
        """
        return set(vs.actor_id for vs in self._my_signals.values())
